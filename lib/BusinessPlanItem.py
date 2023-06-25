import math
import uuid

from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.utils import unwrap


class ItemType:
    Income = 1
    Expense = 2
    ItemsCount = 3

    @staticmethod
    def desc(itemType: int) -> str:
        if itemType == ItemType.Income:
            return "Income"
        elif itemType == ItemType.Expense:
            return "Expense"
        else:
            return ""


class Frequency:
    Weekly = 1
    OnceInTwoWeeks = 2
    TwiceInMonth = 3
    Monthly = 4
    Quarterly = 5
    HalfYear = 6
    Yearly = 7
    ItemsCount = 8

    __desc = {
        Weekly: "Every week",
        OnceInTwoWeeks: "Once in two weeks",
        TwiceInMonth: "Two times per month",
        Monthly: "Once a month",
        Quarterly: "Once a quarter",
        HalfYear: "Once in half a year",
        Yearly: "Once a year",
    }

    @staticmethod
    def desc(freqType: int) -> str:
        return Frequency.__desc.get(freqType, "")


class BusinessPlanItem:
    __freqMultiplier = {
        Frequency.Weekly: 1,
        Frequency.OnceInTwoWeeks: 1.0 / 2,
        Frequency.TwiceInMonth: 12 * 2.0 / 52,
        Frequency.Monthly: 12.0 / 52,
        Frequency.Quarterly: 12.0 / 52 / 4,
        Frequency.HalfYear: 12.0 / 52 / 2,
        Frequency.Yearly: 1.0 / 52,
    }

    def __init__(
        self,
        itemId: uuid.UUID,
        itemType: int,  # FIXME: maybe it should be ItemType
        amount: float,
        name: str,
        freq: int,  # FIXME: maybe it shoule be Frequency
    ) -> None:
        self.__id = itemId
        self.__type = itemType
        self.__amount = amount
        self.__name = name
        self.__freq = freq

    def toXml(self) -> _Element:
        return E.Item(
            id=str(self.__id),
            type=str(self.__type),
            amount=str(self.__amount),
            name=self.__name,
            freq=str(self.__freq),
        )

    @staticmethod
    def fromXml(el: _Element) -> "BusinessPlanItem":
        return BusinessPlanItem(
            uuid.UUID(unwrap(el.get("id"))),
            int(unwrap(el.get("type"))),
            float(unwrap(el.get("amount"))),
            unwrap(el.get("name")),
            int(unwrap(el.get("freq"))),
        )

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def type(self) -> int:
        return self.__type

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def name(self) -> str:
        return self.__name

    @property
    def freq(self) -> int:
        return self.__freq

    @property
    def weeklyValue(self) -> float:
        return math.ceil(
            self.amount * BusinessPlanItem.__freqMultiplier[self.freq]
        )
