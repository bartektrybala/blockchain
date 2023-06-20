from django.urls import include, path
from rest_framework.routers import SimpleRouter

from blockchain.api.views import BlockViewSet, ChanLengthView, TransactionViewSet

router = SimpleRouter()
router.register("blocks", BlockViewSet, basename="blocks")
router.register("transactions", TransactionViewSet, basename="transactions")


urlpatterns = [
    path(r"", include(router.urls)),
    path("chain-length/", ChanLengthView.as_view()),
]
