from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(eq=True, frozen=True)
class Expense:
    value: float
    desc: str
    from_id: int
    to_id: int
    line: str = ""
    manual: bool = False
    date: datetime.datetime = field(default_factory=datetime.datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
