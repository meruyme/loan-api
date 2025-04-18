from decimal import Decimal
from rest_framework import status

from loanmanagement.testing.generic_test_case import GenericTestCase
from loanmanagement.testing.helpers import create_test_payment
from loans.models import LoanPayment


class CreatePaymentTestCase(GenericTestCase):
    def test_cant_create_payment_with_negative_amount(self):
        self.login(self.user1.username)
        response = self.client.post(
            "/api/payments/",
            {
                "amount": -1,
                "loan": self.loan_for_user1.id
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_create_payment_for_loan_of_another_client(self):
        self.login(self.user1.username)
        response = self.client.post(
            "/api/payments/",
            {
                "amount": 1,
                "loan": self.loan_for_user2.id
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_create_payment_for_loan_already_paid(self):
        self.login(self.user1.username)

        self.loan_for_user1.is_already_paid = True
        self.loan_for_user1.save()

        response = self.client.post(
            "/api/payments/",
            {
                "amount": 1,
                "loan": self.loan_for_user1.id
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_create_payment_if_amount_is_bigger_than_outstanding_balance(self):
        self.login(self.user1.username)

        response = self.client.post(
            "/api/payments/",
            {
                "amount": 100000,
                "loan": self.loan_for_user1.id
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_payment_successfully(self):
        self.login(self.user1.username)

        response = self.client.post(
            "/api/payments/",
            {
                "amount": 1000,
                "loan": self.loan_for_user1.id
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.loan_for_user1.payments.all().exists())


class UpdatePaymentTestCase(GenericTestCase):
    def setUp(self):
        super().setUp()
        self.payment_for_loan_user1 = create_test_payment(
            self.loan_for_user1
        )

    def test_cant_update_payment_of_different_client(self):
        self.login(self.user2.username)
        response = self.client.patch(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
            {
                "amount": 1,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_update_payment_if_already_paid(self):
        self.login(self.user1.username)

        self.loan_for_user1.is_already_paid = True
        self.loan_for_user1.save()

        response = self.client.patch(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
            {
                "amount": 1,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_update_payment_amount_if_outstanding_balance_gets_negative(self):
        self.login(self.user1.username)
        response = self.client.patch(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
            {
                "amount": 100000,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_update_payment_successfully(self):
        self.login(self.user1.username)
        response = self.client.patch(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
            {
                "amount": 1000,
            },
            content_type="application/json",
        )
        self.payment_for_loan_user1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.payment_for_loan_user1.amount, Decimal(1000))


class GetPaymentTestCase(GenericTestCase):
    def setUp(self):
        super().setUp()
        self.payment_for_loan_user1 = create_test_payment(
            self.loan_for_user1
        )

    def test_cant_get_payment_of_different_client(self):
        self.login(self.user2.username)
        response = self.client.get(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_get_payment_successfully(self):
        self.login(self.user1.username)
        response = self.client.get(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeletePaymentTestCase(GenericTestCase):
    def setUp(self):
        super().setUp()
        self.payment_for_loan_user1 = create_test_payment(
            self.loan_for_user1
        )

    def test_cant_delete_payment_of_different_client(self):
        self.login(self.user2.username)
        response = self.client.delete(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_delete_payment_if_already_paid(self):
        self.login(self.user1.username)

        self.loan_for_user1.is_already_paid = True
        self.loan_for_user1.save()

        response = self.client.delete(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_delete_payment_successfully(self):
        self.login(self.user1.username)

        payment_id = self.payment_for_loan_user1.id

        response = self.client.delete(
            f"/api/payments/{self.payment_for_loan_user1.id}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(LoanPayment.objects.filter(id=payment_id).exists())
