import logging
import typing as ty
import uuid

import lxml.etree as etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.models.business_plan_item import BusinessPlanItem, ItemType, Frequency


class BusinessPlan:
    def __init__(self, fname: str) -> None:
        self._items: list[BusinessPlanItem] = []
        self._fname = fname
        self._load()

    def _load(self) -> None:
        try:
            doc = etree.parse(self._fname)
        except Exception:
            logging.exception("Exception while reading business plan data")
            return

        for el in ty.cast(list[_Element], doc.xpath("//Item")):
            try:
                item = BusinessPlanItem.from_xml(el)
                self._items.append(item)
            except Exception:
                logging.exception("Exception while parsing BusinessPlanItem")
                continue

    def save(self) -> None:
        doc = E.BusinessPlan()
        doc.extend([item.to_xml() for item in self._items])
        # FIXME: should write safely here
        etree.ElementTree(doc).write(
            self._fname,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8",
        )

    def add_item(
        self, item_type: ItemType, amount: int, name: str, freq: Frequency
    ) -> ty.Optional[BusinessPlanItem]:
        try:
            item = BusinessPlanItem(uuid.uuid4(), item_type, amount, name, freq)
            self._items.append(item)
            return item
        except Exception:
            logging.exception("Error adding BusinessPlanItem")
            return None

    @property
    def items(self) -> list[BusinessPlanItem]:
        return self._items

    @property
    def weekly_income(self) -> float:
        return sum(
            item.weekly_value
            for item in self._items
            if item.type == ItemType.Income
        )

    @property
    def weekly_expense(self) -> float:
        return sum(
            item.weekly_value
            for item in self._items
            if item.type == ItemType.Expense
        )

    @property
    def weekly_envelope(self) -> float:
        return self.weekly_income - self.weekly_expense
