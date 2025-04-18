from decimal import Decimal
from unittest import mock

from django.contrib.auth.models import User
from django.utils import timezone

from loans.models import Bank, Loan, LoanPayment


def create_test_user(username: str) -> User:
    return User.objects.create_user(username=username, password="password")


def create_test_loan(
    user: User, bank: Bank, amount=Decimal(10000), monthly_interest_rate=Decimal(0.01), is_already_paid=False
) -> Loan:
    return Loan.objects.create(
        client=user,
        bank=bank,
        amount=amount,
        monthly_interest_rate=monthly_interest_rate,
        ip_address="127.0.0.1",
        is_already_paid=is_already_paid,
    )


def create_test_payment(
    loan: Loan, amount=Decimal(200), paid_at=None
) -> LoanPayment:
    if not paid_at:
        paid_at = timezone.now()

    with mock.patch('django.utils.timezone.now', mock.Mock(return_value=paid_at)):
        return LoanPayment.objects.create(
            loan=loan,
            amount=amount,
        )
