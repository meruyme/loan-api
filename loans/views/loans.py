from rest_framework import viewsets, status
from rest_framework.response import Response

from loans.models import Loan, LoanPayment
from loans.serializers import LoanSerializer, LoanPaymentSerializer


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer

    def get_queryset(self):
        return Loan.objects.filter(client=self.request.user).prefetch_related("payments").order_by("requested_at")


class LoanPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = LoanPaymentSerializer

    def get_queryset(self):
        return LoanPayment.objects.filter(loan__client=self.request.user).order_by("paid_at")

    def destroy(self, request, *args, **kwargs):
        payment = self.get_object()
        if payment.loan.is_already_paid:
            return Response({"message": "Loan is already paid."}, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)
