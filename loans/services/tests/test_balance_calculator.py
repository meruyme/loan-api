from decimal import Decimal
from unittest import mock

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from loanmanagement.testing.generic_test_case import GenericTestCase
from loanmanagement.testing.helpers import create_test_payment
from loans.services.balance_calculator import calculate_outstanding_balance


class OutstandingBalanceCalculatorTestCase(GenericTestCase):
    def setUp(self):
        super().setUp()
        for month in range(3):
            create_test_payment(
                self.loan_for_user1, paid_at=self.loan_for_user1.requested_at + relativedelta(months=month)
            )

    def test_outstanding_balance_is_correctly_calculated(self):
        mocked_now = timezone.now() + relativedelta(months=2)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked_now)):
            outstanding_balance = calculate_outstanding_balance(
                self.loan_for_user1.requested_at,
                self.loan_for_user1.monthly_interest_rate,
                self.loan_for_user1.amount,
                list(self.loan_for_user1.payments.all())
            )

        self.assertEqual(round(outstanding_balance, 2), round(Decimal(9690.93), 2))
