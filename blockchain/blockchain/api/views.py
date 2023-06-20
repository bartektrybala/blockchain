from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from blockchain.api.serializers import BlockSerializer, TransactionSerializer
from blockchain.models import Block, Transaction


class BlockViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Block.objects.all()
    lookup_field = "previous_hash"
    serializer_class = BlockSerializer
    permission_classes = [
        AllowAny,
    ]


class TransactionViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        AllowAny,
    ]
