import uuid
import math
from lxml.builder import E

class ItemType:
    Income = 1
    Expense = 2
    ItemsCount = 3

    @classmethod
    def desc(cls, itemType):
        if itemType == ItemType.Income:
            return 'Income'
        elif itemType == ItemType.Expense:
            return 'Expense'
        else:
            return ''

class Frequency:
    Weekly = 1
    OnceInTwoWeeks = 2
    TwiceInMonth = 3
    Monthly = 4
    Quarterly = 5
    HalfYear = 6
    Yearly = 7
    ItemsCount = 8

    __desc = { Weekly: "Every week",
        OnceInTwoWeeks: 'Once in two weeks',
        TwiceInMonth: 'Two times per month',
        Monthly: 'Once a month',
        Quarterly: 'Once a quarter',
        HalfYear: 'Once in half a year',
        Yearly: 'Once a year',
    }

    @classmethod
    def desc(cls, freqType):
        if freqType in Frequency.__desc:
            return Frequency.__desc[freqType]
        else:
            return ''

class BusinessPlanItem:
    __freqMultiplier = {
        Frequency.Weekly : 1,
        Frequency.OnceInTwoWeeks: 1.0/2,
        Frequency.TwiceInMonth: 12*2.0/52,
        Frequency.Monthly: 12.0/52,
        Frequency.Quarterly: 12.0/52/4,
        Frequency.HalfYear: 12.0/52/2,
        Frequency.Yearly: 1.0/52,
    }

    def __init__(self, itemId, itemType, amount, name, freq):
        self.__id = itemId
        self.__type = itemType
        self.__amount = amount
        self.__name = name
        self.__freq = freq

    def toSaveLine(self):
        return '{0}\t{1}\t{2}\t{3}\t{4}'.format(self.__id, self.__type, self.__amount, self.__name, self.__freq)

    def toXml(self):
        return E.Item(
            id=str(self.__id),
            type=str(self.__type),
            amount=str(self.__amount),
            name=self.__name,
            freq=str(self.__freq))

    @classmethod
    def fromXml(cls, el):
        return BusinessPlanItem(
            uuid.UUID(el.get("id")),
            int(el.get("type")),
            float(el.get("amount")),
            el.get("name"),
            int(el.get("freq")))

    @classmethod
    def fromSaveLine(cls, line):
        parts = line.split('\t')
        return BusinessPlanItem(uuid.UUID(parts[0]), int(parts[1]), int(parts[2]), parts[3], int(parts[4]))

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    @property
    def amount(self):
        return self.__amount

    @property
    def name(self):
        return self.__name

    @property
    def freq(self):
        return self.__freq

    @property
    def weeklyValue(self):
        return math.ceil(self.amount*BusinessPlanItem.__freqMultiplier[self.freq])

