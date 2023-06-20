from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from blockchain.api.serializers import BlockSerializer, TransactionSerializer
from blockchain.models import Block, Chain, Transaction


class BlockViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Block.objects.all()
    lookup_field = "previous_hash"
    serializer_class = BlockSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_object(self):
        """
        Override this method to convert lookup_field into bytes.
        """
        try:
            self.kwargs[self.lookup_field] = bytes(
                self.kwargs[self.lookup_field], "utf-8"
            )
        except TypeError:
            pass
        return super().get_object()


class TransactionViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        AllowAny,
    ]


class ChanLengthView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self, request):
        chain = Chain.objects.first()
        return Response({"length": len(chain.blocks)})
