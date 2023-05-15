import json
from dataclasses import dataclass

from example_schema.converter import converter


@dataclass
class BaseClass:
    def to_string(self):
        return json.dumps(converter.unstructure(self))
