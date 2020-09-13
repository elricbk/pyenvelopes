from __future__ import annotations

from lxml.builder import E
from lxml.etree import ElementBase

import dataclasses
import datetime
import dateutil.parser
import lxml
import uuid


@dataclasses.dataclass
class Expense:
    id: uuid.UUID
    date: datetime.datetime
    value: float
    desc: str
    fromId: int
    toId: int
    line: str = ''
    manual: bool = True

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def fromXml(cls, el) -> Expense:
        return Expense(
            uuid.UUID(el.get("id")),
            dateutil.parser.parse(el.get("date")),
            float(el.get("value")),
            el.get("desc"),
            int(el.get("fromId")),
            int(el.get("toId")),
            el.get("line"),
            el.get("manual") == "True",
        )

    def toXml(self) -> ElementBase:
        return E.Expense(
            id=str(self.id),
            date=str(self.date),
            value=str(self.value),
            desc=self.desc,
            fromId=str(self.fromId),
            toId=str(self.toId),
            line=self.line,
            manual=str(self.manual)
        )
