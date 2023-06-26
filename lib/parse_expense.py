import re
from dataclasses import dataclass
from typing import Optional

from .well_known_envelope import WellKnownEnvelope

RGX_SHORT = re.compile(r"(\d+)\s+(\w.*)", re.U)
RGX_ENVELOPE = re.compile(r"\+?(\d+)\s+(\w.*)\s+%(\S+)", re.U)
RGX_FULL = re.compile(r"(\d+)\s+(\S.*)\s+%(\S+)\s+%(\S+)", re.U)


@dataclass
class ParsedExpense:
    amount: str
    comment: str
    from_envelope: WellKnownEnvelope | str
    to_envelope: WellKnownEnvelope | str


def parse_expense(line: str) -> ParsedExpense:
    line = line.strip()

    if res := RGX_FULL.match(line):
        return ParsedExpense(
            res.group(1), res.group(2), res.group(3), res.group(4)
        )
    elif res := RGX_ENVELOPE.match(line):
        if line.startswith("+"):
            return ParsedExpense(
                res.group(1),
                res.group(2),
                WellKnownEnvelope.Income,
                res.group(3),
            )
        else:
            return ParsedExpense(
                res.group(1),
                res.group(2),
                res.group(3),
                WellKnownEnvelope.TrashBin,
            )
    elif res := RGX_SHORT.match(line):
        return ParsedExpense(
            res.group(1),
            res.group(2),
            WellKnownEnvelope.ThisWeek,
            WellKnownEnvelope.TrashBin,
        )

    raise Exception("Wrong format")
