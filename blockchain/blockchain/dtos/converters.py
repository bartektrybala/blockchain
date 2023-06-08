from datetime import datetime
from decimal import Decimal

from cattrs import Converter

converter = Converter()

# datetime is not a primitive type, so we need to register hooks for it
converter.register_unstructure_hook(datetime, lambda dt: dt.isoformat())
converter.register_structure_hook(datetime, lambda s, _: datetime.fromisoformat(s))

converter.register_unstructure_hook(bytes, lambda dt: int.from_bytes(dt))
converter.register_structure_hook(bytes, lambda s, _: s.to_bytes(32))

converter.register_unstructure_hook(Decimal, str)
converter.register_structure_hook(Decimal, lambda x, _: Decimal(x))
