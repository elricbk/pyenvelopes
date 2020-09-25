import uuid
from lxml.builder import E # type: ignore

class ExpenseRule:
    def __init__(self, ruleId, amount, fromId, toId):
        self.__id = ruleId
        self.__amount = amount
        self.__fromId = fromId
        self.__toId = toId

    def toXml(self):
        return E.ExpenseRule(
            id=str(self.__id), 
            amount=str(self.__amount), 
            fromId=str(self.__fromId), 
            toId=str(self.__toId)) 

    @classmethod
    def fromXml(cls, el):
        return ExpenseRule(
            uuid.UUID(el.get("id")), 
            float(el.get("amount")), 
            int(el.get("fromId")), 
            int(el.get("toId")))

    @property
    def id(self):
        return self.__id

    @property
    def amount(self):
        return self.__amount

    @property
    def fromId(self):
        return self.__fromId

    @property
    def toId(self):
        return self.__toId

