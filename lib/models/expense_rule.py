from __future__ import annotations

import uuid
from dataclasses import dataclass

from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.utils import unwrap


@dataclass
class ExpenseRule:
    id: uuid.UUID
    amount: float
    from_id: int
    to_id: int
