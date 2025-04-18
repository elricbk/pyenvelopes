from __future__ import annotations

import enum
import math
import uuid
from dataclasses import dataclass


class ItemType(enum.IntEnum):
    Income = 1
    Expense = 2


class Frequency(enum.IntEnum):
    Weekly = 1
    OnceInTwoWeeks = 2
    TwiceInMonth = 3
    Monthly = 4
    Quarterly = 5
    HalfYear = 6
    Yearly = 7


@dataclass
class BusinessPlanItem:
    id: uuid.UUID
    type: ItemType
    amount: float
    name: str
    freq: Frequency

    _freq_multiplier = {
        Frequency.Weekly: 1,
        Frequency.OnceInTwoWeeks: 1.0 / 2,
        Frequency.TwiceInMonth: 12 * 2.0 / 52,
        Frequency.Monthly: 12.0 / 52,
        Frequency.Quarterly: 12.0 / 52 / 4,
        Frequency.HalfYear: 12.0 / 52 / 2,
        Frequency.Yearly: 1.0 / 52,
    }

    @property
    def weekly_value(self) -> float:
        return math.ceil(
            self.amount * BusinessPlanItem._freq_multiplier[self.freq]
        )
