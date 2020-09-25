from lxml.builder import E # type: ignore
from lxml.etree import ElementBase
import dataclasses

EnvelopeId = int

@dataclasses.dataclass
class Envelope:
    id: EnvelopeId
    name: str
    desc: str

    @classmethod
    def fromXml(cls, el: ElementBase) -> 'Envelope':
        return Envelope(int(el.get("id")), el.get("name"), el.get("desc"))

    def toXml(self) -> ElementBase:
        return E.Envelope(id=str(self.id), name=self.name, desc=self.desc)
