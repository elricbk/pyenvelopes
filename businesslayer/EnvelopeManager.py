import datetime
import logging
from lxml import etree
from lxml.builder import E
from Envelope import Envelope


class EnvelopeManager:
    __envelopeFileName = 'data/envelopes.xml'

    def __init__(self):
        self.__envelopes = {1: Envelope.Income(), 2: Envelope.Expense(), 3: Envelope.Leftover()}
        self.__expMgr = None
        self.__loadSavedEnvelopes()

    def __maxId(self):
        return max(self.__envelopes.keys())

    def setExpenseManager(self, expMgr):
        self.__expMgr = expMgr

    def addEnvelope(self, name, desc=''):
        logging.info("Adding envelope with name %s, id will be %d", name, self.__maxId())
        if name.lower() in (v.name.lower() for v in self.envelopes.values()):
            raise RuntimeError("Envelope with given name already exists")
        e = Envelope.fromData(self.__maxId() + 1, name, desc)
        self.__envelopes[e.id] = e
        self.__saveAllEnvelopes()
        return e

    def __saveAllEnvelopes(self):
        doc = E.Envelopes()
        doc.extend([env.toXml() for env in self.__envelopes.values()])
        etree.ElementTree(doc).write(EnvelopeManager.__envelopeFileName, pretty_print=True, encoding='utf-8')

    def __loadSavedEnvelopes(self):
        try:
            doc = etree.parse(EnvelopeManager.__envelopeFileName)
        except Exception as e:
            print(e)
            return

        for el in doc.xpath("//Envelope"):
            try:
                env = Envelope.fromXml(el)
                self.__envelopes[env.id] = env
            except Exception as e:
                print(e)

    @property
    def envelopes(self):
        return self.__envelopes

    def markEnvelopeAsArchive(self, envId):
        pass

    def idForEnvName(self, envName):
        #print(u"Searching for envelope '{0}'".format(envName))
        # FIXME: envelope name is not unique, it may lead to problems
        for k, v in self.__envelopes.items():
            if envName.lower() == v.name.lower():
                return k
        raise Exception('No envelope with given name')

    def envNameForId(self, envId):
        return self.__envelopes[envId].name

    def envelopeValue(self, envId):
        value = 0
        for ex in self.__expMgr.expenses:
            if ex.fromId == envId:
                value -= ex.value
            if ex.toId == envId:
                value += ex.value
        return value

    @staticmethod
    def _weekEnvelopeName(isoDate):
        year = isoDate[0]
        weekNum = isoDate[1]
        return "Week_{0}_{1}".format(year, weekNum)

    @property
    def currentEnvelope(self):
        isoDate = datetime.datetime.now().isocalendar()
        envName = self._weekEnvelopeName(isoDate)
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)

    @property
    def lastWeekEnvelope(self):
        isoDate = (datetime.datetime.now() - datetime.timedelta(days=7)).isocalendar()
        envName = self._weekEnvelopeName(isoDate)
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)

    def envelopeForDate(self, date):
        envName = self.weekEnvelopName(date.isodate())
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)
