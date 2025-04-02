import logging
import typing as ty
import uuid

import lxml.etree as etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from ....models.business_plan_item import BusinessPlanItem, ItemType, Frequency
from lxml.builder import E  # type: ignore
from ....utils import unwrap
import uuid


def business_plan_item_to_xml(item: BusinessPlanItem) -> _Element:
    """Converts a BusinessPlanItem object to an XML element."""
    return E.Item(
        id=str(item.id),
        type=item.type.name,
        amount=str(item.amount),
        name=item.name,
        freq=item.freq.name,
    )


def xml_to_business_plan_item(el: _Element) -> BusinessPlanItem:
    """Converts an XML element to a BusinessPlanItem object."""
    return BusinessPlanItem(
        uuid.UUID(unwrap(el.get("id"))),
        ItemType[unwrap(el.get("type"))],
        int(unwrap(el.get("amount"))),
        unwrap(el.get("name")),
        Frequency[unwrap(el.get("freq"))],
    )




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
                item = xml_to_business_plan_item(el)
                self._items.append(item)
            except Exception:
                logging.exception("Exception while parsing BusinessPlanItem")
                continue

    def save(self) -> None:
        doc = E.BusinessPlan()
        doc.extend([business_plan_item_to_xml(item) for item in self._items])
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
