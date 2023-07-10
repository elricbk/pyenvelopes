from __future__ import annotations

import dataclasses

from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.utils import unwrap

EnvelopeId = int


@dataclasses.dataclass
class Envelope:
    id: EnvelopeId
    name: str
    desc: str

    @classmethod
    def from_xml(cls, el: _Element) -> Envelope:
        return Envelope(
            int(unwrap(el.get("id"))),
            unwrap(el.get("name")),
            unwrap(el.get("desc")),
        )

    def to_xml(self) -> _Element:
        return E.Envelope(id=str(self.id), name=self.name, desc=self.desc)
