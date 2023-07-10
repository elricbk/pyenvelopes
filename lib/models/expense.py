from __future__ import annotations

import datetime
import uuid
from dataclasses import dataclass, field

import dateutil.parser
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.utils import unwrap


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

    @classmethod
    def from_xml(cls, el: _Element) -> Expense:
        return Expense(
            float(unwrap(el.get("value"))),
            unwrap(el.get("desc")),
            int(unwrap(el.get("fromId"))),
            int(unwrap(el.get("toId"))),
            unwrap(el.get("line")),
            unwrap(el.get("manual")) == "True",
            dateutil.parser.parse(unwrap(el.get("date"))),
            uuid.UUID(unwrap(el.get("id"))),
        )

    def to_xml(self) -> _Element:
        return E.Expense(
            id=str(self.id),
            date=str(self.date),
            value=str(self.value),
            desc=self.desc,
            fromId=str(self.from_id),
            toId=str(self.to_id),
            line=self.line,
            manual=str(self.manual),
        )
