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

    def to_xml(self) -> _Element:
        return E.ExpenseRule(
            id=str(self.id),
            amount=str(self.amount),
            fromId=str(self.from_id),
            toId=str(self.to_id),
        )

    @staticmethod
    def from_xml(el: _Element) -> ExpenseRule:
        return ExpenseRule(
            uuid.UUID(unwrap(el.get("id"))),
            float(unwrap(el.get("amount"))),
            int(unwrap(el.get("fromId"))),
            int(unwrap(el.get("toId"))),
        )
