from collections import defaultdict
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from dateutil import rrule
from django.utils import timezone

from loans.signals import update_loan_finished_payment


class Bank(models.Model):
    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name


class Loan(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=5)
    monthly_interest_rate = models.DecimalField(max_digits=7, decimal_places=5)
    ip_address = models.CharField(max_length=32)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name="loans")
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name="loans")
    is_already_paid = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.id)

    @property
    def outstanding_balance(self) -> Decimal:
        from loans.services.balance_calculator import calculate_outstanding_balance

        if self.is_already_paid:
            return Decimal(0)

        return calculate_outstanding_balance(
            self.requested_at, self.monthly_interest_rate, self.amount, list(self.payments.all())
        )


class LoanPayment(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=5)
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, related_name="payments")
    paid_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.id)


post_save.connect(update_loan_finished_payment, sender=LoanPayment)
