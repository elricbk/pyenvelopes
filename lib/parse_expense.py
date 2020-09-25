from dataclasses import dataclass
from typing import Optional
import re

RGX_SHORT = re.compile(r'(\d+)\s+(\w.*)', re.U)
RGX_ENVELOPE = re.compile(r'\+?(\d+)\s+(\w.*)\s+%(\S+)', re.U)
RGX_FULL = re.compile(r'(\d+)\s+(\S.*)\s+%(\S+)\s+%(\S+)', re.U)

@dataclass
class ParsedExpense:
    amount: str
    comment: str
    from_envelope: Optional[str]
    to_envelope: str

def parse_expense(line: str) -> ParsedExpense:
    line = line.strip()
    income = 'доход'
    trash_bin = 'корзина'

    if res := RGX_FULL.match(line):
        return ParsedExpense(
            res.group(1),
            res.group(2),
            res.group(3),
            res.group(4)
        )
    elif res := RGX_ENVELOPE.match(line):
        if line.startswith('+'):
            return ParsedExpense(
                res.group(1),
                res.group(2),
                income,
                res.group(3)
            )
        else:
            return ParsedExpense(
                res.group(1),
                res.group(2),
                res.group(3),
                trash_bin
            )
    elif res := RGX_SHORT.match(line):
        return ParsedExpense(
            res.group(1),
            res.group(2),
            None,
            trash_bin
        )

    raise Exception('Wrong format')
