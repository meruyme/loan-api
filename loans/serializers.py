from decimal import Decimal

from rest_framework import serializers

from loans.models import Loan, LoanPayment
from loans.services.common_services import get_ip_address_from_request
from loans.services.balance_calculator import calculate_outstanding_balance


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "id",
            "amount",
            "monthly_interest_rate",
            "outstanding_balance",
            "ip_address",
            "bank",
            "client",
            "requested_at",
            "is_already_paid",
        )
        read_only_fields = (
            "id",
            "ip_address",
            "requested_at",
            "client",
            "is_already_paid",
        )

    def validate_amount(self, amount):
        if self.instance and not self.__is_amount_valid(amount):
            raise serializers.ValidationError("Invalid amount.")
        return amount

    def create(self, validated_data):
        ip_address = get_ip_address_from_request(self.context["request"])
        user = self.context["request"].user
        loan = Loan.objects.create(ip_address=ip_address, client=user, **validated_data)

        return loan

    def __is_amount_valid(self, amount: Decimal) -> bool:
        outstanding_balance = calculate_outstanding_balance(
            self.instance.requested_at,
            self.instance.self.monthly_interest_rate,
            amount,
            list(self.instance.payments.all())
        )

        return outstanding_balance >= 0


class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = (
            "id",
            "amount",
            "loan",
            "paid_at",
        )
        read_only_fields = (
            "id",
        )

    def validate(self, data):
        user = self.context["request"].user
        loan_id = data["loan"]
        amount = data["amount"]
        loan = Loan.objects.filter(id=loan_id, client=user).first()

        if not loan:
            raise serializers.ValidationError("Loan not found.")

        if self.__is_loan_already_paid(loan):
            raise serializers.ValidationError("Loan is already paid.")

        if not self.__is_balance_bigger_than_amount(loan, amount):
            raise serializers.ValidationError("Amount must be smaller of equal to outstanding balance.")

    @staticmethod
    def __is_loan_already_paid(loan: Loan) -> bool:
        return loan.is_already_paid

    @staticmethod
    def __is_balance_bigger_than_amount(loan: Loan, amount: Decimal) -> bool:
        return loan.outstanding_balance >= amount
