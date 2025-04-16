from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from dateutil import rrule
from django.utils import timezone


class Bank(models.Model):
    name = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.name


class Loan(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    monthly_interest_rate = models.DecimalField(max_digits=7, decimal_places=5)
    ip_address = models.CharField(max_length=32)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name='loans')
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='loans')
    requested_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.id

    @property
    def outstanding_balance(self):
        balance = self.amount
        months = rrule.rrule(rrule.MONTHLY, dtstart=self.requested_at, until=timezone.now())
        payments_by_month = {
            payment.paid_at.strftime('%m-%Y'): payment.amount
            for payment in self.payments.all()
        }

        for month in months:
            payment_of_month = payments_by_month.get(month.strftime('%m-%Y'), Decimal(0))
            balance = (balance - payment_of_month) * (Decimal(1) + self.monthly_interest_rate)

        return balance


class LoanPayment(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, related_name='payments')
    paid_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.id
