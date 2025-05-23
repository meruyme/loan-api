# Generated by Django 4.2.20 on 2025-04-18 02:52

from django.db import migrations, models
import loans.validators


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_loan_is_already_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='amount',
            field=models.DecimalField(decimal_places=5, max_digits=15, validators=[loans.validators.GreaterThanValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='loan',
            name='monthly_interest_rate',
            field=models.DecimalField(decimal_places=5, max_digits=7, validators=[loans.validators.GreaterThanValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='loanpayment',
            name='amount',
            field=models.DecimalField(decimal_places=5, max_digits=15, validators=[loans.validators.GreaterThanValueValidator(0)]),
        ),
    ]
