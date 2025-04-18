from decimal import Decimal
from loanmanagement.testing.generic_test_case import GenericTestCase
from loanmanagement.testing.helpers import create_test_payment


class LoanTestCase(GenericTestCase):
    def test_loan_outstanding_balance_returns_zero_if_already_paid(self):
        self.loan_for_user1.is_already_paid = True
        self.loan_for_user1.save()

        self.assertEqual(self.loan_for_user1.outstanding_balance, Decimal(0))

    def test_loan_is_set_to_paid_after_paying_all_debt(self):
        create_test_payment(
            self.loan_for_user1, amount=Decimal(10000)
        )

        self.loan_for_user1.refresh_from_db()

        self.assertTrue(self.loan_for_user1.is_already_paid)
