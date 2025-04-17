from rest_framework.routers import DefaultRouter
from loans.views import LoanViewSet, LoanPaymentViewSet

router = DefaultRouter()
router.register('loans', LoanViewSet, basename='loans')
router.register('loan-payments', LoanPaymentViewSet, basename='loan_payments')
urlpatterns = router.urls
