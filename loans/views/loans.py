from rest_framework import viewsets

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
