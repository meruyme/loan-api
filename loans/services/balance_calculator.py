from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from dateutil import rrule
from django.utils import timezone


def calculate_outstanding_balance(
    loan_initial_date: datetime, monthly_interest_rate: Decimal, amount: Decimal, payments: list
) -> Decimal:
    balance = amount
    months = rrule.rrule(rrule.MONTHLY, dtstart=loan_initial_date, until=timezone.now())
    payments_by_month = defaultdict(Decimal)

    for payment in payments:
        payments_by_month[payment.paid_at.strftime("%m-%Y")] += payment.amount

    for month in months:
        payment_of_month = payments_by_month.get(month.strftime("%m-%Y"), Decimal(0))
        balance = (balance - payment_of_month) * (Decimal(1) + monthly_interest_rate)

    return balance
