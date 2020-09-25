from __future__ import annotations

from lxml.builder import E
from lxml.etree import ElementBase

from dataclasses import dataclass, field
import datetime
import dateutil.parser
import uuid


@dataclass(eq=True, frozen=True)
class Expense:
    value: float
    desc: str
    fromId: int
    toId: int
    line: str = ''
    manual: bool = False
    date: datetime.datetime = field(default_factory=datetime.datetime.now)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def fromXml(cls, el: ElementBase) -> Expense:
        return Expense(
            float(el.get("value")),
            el.get("desc"),
            int(el.get("fromId")),
            int(el.get("toId")),
            el.get("line"),
            el.get("manual") == "True",
            dateutil.parser.parse(el.get("date")),
            uuid.UUID(el.get("id")),
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
