from BusinessPlanItem import BusinessPlanItem, ItemType, Frequency
import uuid
from lxml import etree
from lxml.builder import E

class BusinessPlan:
    __itemsFileName = 'business_plan.xml'

    def __init__(self):
        self.__items = []
        self.__load()

    def __load(self):
        try:
            doc = etree.parse(BusinessPlan.__itemsFileName)
        except Exception as e:
            print(e)
            return

        for el in doc.xpath("//Item"):
            try:
                item = BusinessPlanItem.fromXml(el)
                self.__items.append(item)
            except Exception as e:
                print(e)
                continue

    def save(self):
        doc = E.BusinessPlan()
        doc.extend([item.toXml() for item in self.__items])
        etree.ElementTree(doc).write(BusinessPlan.__itemsFileName, pretty_print=True)

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
