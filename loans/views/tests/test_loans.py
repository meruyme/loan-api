from decimal import Decimal
from rest_framework import status

from loanmanagement.testing.generic_test_case import GenericTestCase
from loanmanagement.testing.helpers import create_test_payment
from loans.models import Loan, LoanPayment


class CreateLoanTestCase(GenericTestCase):
    def test_cant_create_loan_with_negative_amount(self):
        self.login(self.user1.username)
        response = self.client.post(
            "/api/loans/",
            {
                "amount": -1,
                "monthly_interest_rate": 0.02,
                "bank": self.bank.id
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_create_loan_with_negative_interest_rate(self):
        self.login(self.user1.username)
        response = self.client.post(
            "/api/loans/",
            {
                "amount": 1,
                "monthly_interest_rate": -0.02,
                "bank": self.bank.id
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_loan_successfully(self):
        self.login(self.user1.username)
        response = self.client.post(
            "/api/loans/",
            {
                "amount": 1,
                "monthly_interest_rate": 0.02,
                "bank": self.bank.id
            },
            content_type="application/json",
        )
        body = response.json()
        loan_id = body["id"]
        loan = Loan.objects.filter(id=loan_id).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(loan)
        self.assertEqual(loan.amount, Decimal(body["amount"]))
        self.assertEqual(loan.monthly_interest_rate, Decimal(body["monthly_interest_rate"]))
        self.assertEqual(loan.bank_id, self.bank.id)
        self.assertEqual(loan.client_id, self.loan_for_user1.id)


class UpdateLoanTestCase(GenericTestCase):
    def test_cant_update_loan_of_different_client(self):
        self.login(self.user1.username)
        response = self.client.patch(
            f"/api/loans/{self.loan_for_user2.id}/",
            {
                "amount": 1,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_update_loan_if_already_paid(self):
        self.login(self.user1.username)
        self.loan_for_user1.is_already_paid = True
        self.loan_for_user1.save()
        response = self.client.patch(
            f"/api/loans/{self.loan_for_user1.id}/",
            {
                "amount": 1,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_update_loan_amount_if_outstanding_balance_gets_negative(self):
        self.login(self.user1.username)
        create_test_payment(self.loan_for_user1, amount=Decimal(500))
        response = self.client.patch(
            f"/api/loans/{self.loan_for_user1.id}/",
            {
                "amount": 1,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_update_loan_successfully(self):
        self.login(self.user1.username)
        response = self.client.patch(
            f"/api/loans/{self.loan_for_user1.id}/",
            {
                "amount": 1000,
                "monthly_interest_rate": 1,
            },
            content_type="application/json",
        )
        self.loan_for_user1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.loan_for_user1.amount, Decimal(1000))
        self.assertEqual(self.loan_for_user1.monthly_interest_rate, Decimal(1))


class GetLoanTestCase(GenericTestCase):
    def test_cant_get_loan_of_different_client(self):
        self.login(self.user1.username)
        response = self.client.get(
            f"/api/loans/{self.loan_for_user2.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_get_loan_successfully(self):
        self.login(self.user1.username)
        response = self.client.get(
            f"/api/loans/{self.loan_for_user1.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteLoanTestCase(GenericTestCase):
    def setUp(self):
        super().setUp()
        self.payment_for_loan_user1 = create_test_payment(
            self.loan_for_user1
        )

    def test_cant_delete_loan_of_different_client(self):
        self.login(self.user1.username)
        response = self.client.delete(
            f"/api/loans/{self.loan_for_user2.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_delete_loan_successfully(self):
        self.login(self.user1.username)

        loan_id = self.loan_for_user1.id
        payment_id = self.payment_for_loan_user1.id

        response = self.client.delete(
            f"/api/loans/{self.loan_for_user1.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Loan.objects.filter(id=loan_id).exists())
        self.assertFalse(LoanPayment.objects.filter(id=payment_id).exists())
