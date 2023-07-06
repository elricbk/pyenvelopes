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
    fromId: int
    toId: int

    def toXml(self) -> _Element:
        return E.ExpenseRule(
            id=str(self.id),
            amount=str(self.amount),
            fromId=str(self.fromId),
            toId=str(self.toId),
        )

    @staticmethod
    def fromXml(el: _Element) -> ExpenseRule:
        return ExpenseRule(
            uuid.UUID(unwrap(el.get("id"))),
            float(unwrap(el.get("amount"))),
            int(unwrap(el.get("fromId"))),
            int(unwrap(el.get("toId"))),
        )
