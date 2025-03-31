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
