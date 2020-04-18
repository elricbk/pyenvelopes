import datetime
import re
import uuid
from lxml.builder import E


class Expense:
    def __init__(self, data):
        #print(data)
        self.__id = data[0]
        self.__date = data[1]
        self.__value = float(data[2])
        self.__desc = data[3]
        self.__fromId = int(data[4])
        self.__toId = int(data[5])
        if len(data) > 6:
            self.__line = data[6]
        else:
            self.__line = ''
        if len(data) > 7:
            self.__manual = data[7]
        else:
            self.__manual = True


    @classmethod
    def fromSaveLine(cls, line):
        line = line.strip()
        parts = line.split('\t')
        parts[0] = uuid.UUID(parts[0])
        parts[1] = datetime.datetime(*map(int, re.split('[^\d]', parts[1])[:-1]))
        ex = Expense(parts)
        return ex

    def toSaveLine(self):
        saveLineFmt = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}"
        return saveLineFmt.format(self.__id, self.__date, self.__value, self.__desc, self.__fromId, self.__toId,
            self.__line, self.__manual)

    @classmethod
    def fromXml(cls, el):
        parts = [
            uuid.UUID(el.get("id")),
            datetime.datetime(*map(int, re.split('[^\d]', el.get("date"))[:-1])),
            float(el.get("value")),
            el.get("desc"),
            int(el.get("fromId")),
            int(el.get("toId")),
            el.get("line"),
            el.get("manual") == "True",
        ]
        return Expense(parts)

    def toXml(self):
        return E.Expense(
            id=str(self.__id),
            date=str(self.__date),
            value=str(self.__value),
            desc=self.__desc,
            fromId=str(self.__fromId),
            toId=str(self.__toId),
            line=self.__line,
            manual=str(self.__manual))

    @property
    def value(self):
        return self.__value

    @property
    def fromId(self):
        return self.__fromId

    @property
    def toId(self):
        return self.__toId

    @property
    def desc(self):
        return self.__desc

    @property
    def date(self):
        return self.__date

    @property
    def manual(self):
        return self.__manual

    def __str__(self):
        return 'Date="{0}" Value="{1}" Description="{2}" FromId="{3}" ToId="{4}"'.format(
            self.__date.strftime('%c'), self.__value, self.__desc, self.__fromId, self.__toId)
