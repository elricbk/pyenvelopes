import dataclasses


EnvelopeId = int


@dataclasses.dataclass
class Envelope:
    id: EnvelopeId
    name: str
    desc: str
