from dataclasses import dataclass
from datetime import datetime


@dataclass
class Record:
    index: int
    timestamp: datetime
    content: bytes


@dataclass
class Block:
    index: int
    main_hash: bytes
    extra_hashes: list[bytes]
    pow: bytes
    timestamp: datetime
    records: list[Record]
