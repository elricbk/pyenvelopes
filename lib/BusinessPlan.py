import logging
import typing as ty
import uuid

import lxml.etree as etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from .BusinessPlanItem import BusinessPlanItem, ItemType


class BusinessPlan:
    def __init__(self, fname: str) -> None:
        self.__items: list[BusinessPlanItem] = []
        self._fname = fname
        self.__load()

    def __load(self) -> None:
        try:
            doc = etree.parse(self._fname)
        except Exception:
            logging.exception("Exception while reading business plan data")
            return

        for el in ty.cast(list[_Element], doc.xpath("//Item")):
            try:
                item = BusinessPlanItem.fromXml(el)
                self.__items.append(item)
            except Exception:
                logging.exception("Exception while parsing BusinessPlanItem")
                continue

    def save(self) -> None:
        doc = E.BusinessPlan()
        doc.extend([item.toXml() for item in self.__items])
        # FIXME: should write safely here
        etree.ElementTree(doc).write(
            self._fname,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8",
        )

    def addItem(
        self, itemType: int, amount: int, name: str, freq: int
    ) -> ty.Optional[BusinessPlanItem]:
        try:
            item = BusinessPlanItem(uuid.uuid4(), itemType, amount, name, freq)
            self.__items.append(item)
            return item
        except Exception as e:
            print(e)
            return None

    @property
    def items(self) -> list[BusinessPlanItem]:
        return self.__items

    @property
    def weeklyIncome(self) -> float:
        return sum(
            item.weeklyValue
            for item in self.__items
            if item.type == ItemType.Income
        )

    @property
    def weeklyExpense(self) -> float:
        return sum(
            item.weeklyValue
            for item in self.__items
            if item.type == ItemType.Expense
        )

    @property
    def weeklyEnvelope(self) -> float:
        return self.weeklyIncome - self.weeklyExpense
