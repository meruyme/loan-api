from django.db import models
from django.contrib.auth.models import User


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


class LoanPayment(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT, related_name='payments')
    paid_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.id
