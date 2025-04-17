from decimal import Decimal

from rest_framework import serializers

from loans.models import Loan, LoanPayment
from loans.services.common_services import get_ip_address_from_request
from loans.services.balance_calculator import calculate_outstanding_balance


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
        amount = data.get("amount")
        loan = data.get("loan")
        if not loan and self.instance:
            loan = self.instance.loan

        if self.__loan_doesnt_exists(loan):
            raise serializers.ValidationError("Loan not found.")

        if self.__is_loan_already_paid(loan):
            raise serializers.ValidationError("Loan is already paid.")

        if not self.__is_balance_bigger_than_amount(loan, amount):
            raise serializers.ValidationError("Amount must be smaller of equal to outstanding balance.")

        return data

    def __loan_doesnt_exists(self, loan):
        user = self.context["request"].user

        return not loan or (loan.client != user)

    @staticmethod
    def __is_loan_already_paid(loan: Loan) -> bool:
        return loan.is_already_paid

    def __is_balance_bigger_than_amount(self, loan: Loan, amount: Decimal) -> bool:
        from loans.services.balance_calculator import calculate_outstanding_balance

        if not amount:
            return True

        if not self.instance:
            outstanding_balance = loan.outstanding_balance
        else:
            payments = list(LoanPayment.objects.filter(loan_id=loan.id).exclude(id=self.instance.id))
            payments.append(
                LoanPayment(
                    paid_at=self.instance.paid_at,
                    amount=amount
                )
            )

            outstanding_balance = calculate_outstanding_balance(
                loan.requested_at, loan.monthly_interest_rate, loan.amount, payments
            )

        return outstanding_balance >= amount


class LoanSerializer(serializers.ModelSerializer):
    payments = LoanPaymentSerializer(many=True, read_only=True)

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
            "payments",
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
        if not amount:
            return True

        outstanding_balance = calculate_outstanding_balance(
            self.instance.requested_at,
            self.instance.self.monthly_interest_rate,
            amount,
            list(self.instance.payments.all())
        )

        return outstanding_balance >= 0
