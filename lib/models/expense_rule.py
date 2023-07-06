from __future__ import annotations

import uuid

from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.utils import unwrap


class ExpenseRule:
    def __init__(
        self, ruleId: uuid.UUID, amount: float, fromId: int, toId: int
    ) -> None:
        self.__id = ruleId
        self.__amount = amount
        self.__fromId = fromId
        self.__toId = toId

    def toXml(self) -> _Element:
        return E.ExpenseRule(
            id=str(self.__id),
            amount=str(self.__amount),
            fromId=str(self.__fromId),
            toId=str(self.__toId),
        )

    @staticmethod
    def fromXml(el: _Element) -> ExpenseRule:
        return ExpenseRule(
            uuid.UUID(unwrap(el.get("id"))),
            float(unwrap(el.get("amount"))),
            int(unwrap(el.get("fromId"))),
            int(unwrap(el.get("toId"))),
        )

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def fromId(self) -> int:
        return self.__fromId

    @property
    def toId(self) -> int:
        return self.__toId
