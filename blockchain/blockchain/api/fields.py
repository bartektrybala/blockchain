from rest_framework.relations import SlugRelatedField

from blockchain.utils import int_to_bytes


class RelatedPublicKeyField(SlugRelatedField):
    def __init__(self, slug_field="public_key", **kwargs):
        super().__init__(slug_field=slug_field, **kwargs)

    def to_representation(self, obj):
        public_key_bytes: bytes = super().to_representation(obj)
        return int.from_bytes(public_key_bytes, "big")

    def to_internal_value(self, data: int):
        public_key_bytes = int_to_bytes(data)
        return super().to_internal_value(public_key_bytes)
