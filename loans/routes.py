from rest_framework.routers import DefaultRouter
from loans.views import LoanViewSet, LoanPaymentViewSet

router = DefaultRouter()
router.register("loans", LoanViewSet, basename="loans")
router.register("payments", LoanPaymentViewSet, basename="payments")
urlpatterns = router.urls
