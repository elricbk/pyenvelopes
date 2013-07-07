from lxml.builder import E

class Envelope:
    def __init__(self):
        self.__id = -1
        self.__name = ''
        self.__desc = ''
    
    @classmethod
    def fromData(cls, envId, name, desc = ''):
        e = Envelope()
        e.__id = envId
        e.__name = name
        e.__desc = desc
        return e

    @classmethod
    def fromXml(cls, el):
        e = Envelope()
        e.__id = int(el.get("id"))
        e.__name = el.get("name")
        e.__desc = el.get("desc")
        return e

    def toXml(self):
        return E.Envelope(id=str(self.__id), name=self.__name, desc=self.__desc)

    @classmethod
    def Income(cls):
        e = Envelope()
        e.__id = 1
        e.__name = 'Income'
        e.__desc = ''
        return e

    @classmethod
    def Expense(cls):
        e = Envelope()
        e.__id = 2
        e.__name = 'Expense'
        e.__desc = ''
        return e

    @classmethod
    def Leftover(cls):
        e = Envelope()
        e.__id = 3
        e.__name = 'Leftover'
        e.__desc = ''
        return e

    @property
    def id(self): 
        return self.__id

    @property
    def name(self): 
        return self.__name

    @property
    def desc(self): 
        return self.__desc
