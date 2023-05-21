from datetime import datetime

from cattrs import Converter

converter = Converter()

# datetime is not a primitive type, so we need to register hooks for it
converter.register_unstructure_hook(datetime, lambda dt: dt.isoformat())
converter.register_structure_hook(datetime, lambda s, _: datetime.fromisoformat(s))
