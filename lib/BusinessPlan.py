from .BusinessPlanItem import BusinessPlanItem, ItemType, Frequency

import uuid
import lxml.etree as etree
from lxml.builder import E # type: ignore
import logging
import os
import settings


class BusinessPlan:
    __itemsFileName = os.path.join(settings.data_path, 'business_plan.xml')

    def __init__(self):
        self.__items = []
        self.__load()

    def __load(self):
        try:
            doc = etree.parse(BusinessPlan.__itemsFileName)
        except Exception:
            logging.exception("Exception while reading business plan data")
            return

        for el in doc.xpath("//Item"):
            try:
                item = BusinessPlanItem.fromXml(el)
                self.__items.append(item)
            except Exception:
                logging.exception("Exception while parsing BusinessPlanItem")
                continue

    def save(self):
        doc = E.BusinessPlan()
        doc.extend([item.toXml() for item in self.__items])
        # FIXME: should write safely here
        etree.ElementTree(doc).write(
            BusinessPlan.__itemsFileName,
            pretty_print=True,
            xml_declaration=True,
            encoding='UTF-8'
        )

    def addItem(self, itemType, amount, name, freq):
        try:
            item = BusinessPlanItem(uuid.uuid4(), itemType, amount, name, freq)
            self.__items.append(item)
            return item
        except Exception as e:
            print(e)
            return None

    @property
    def items(self):
        return self.__items

    @property
    def weeklyIncome(self):
        return sum([item.weeklyValue for item in self.__items if item.type == ItemType.Income])

    @property
    def weeklyExpense(self):
        return sum([item.weeklyValue for item in self.__items if item.type == ItemType.Expense])

    @property
    def weeklyEnvelope(self):
        return self.weeklyIncome - self.weeklyExpense
