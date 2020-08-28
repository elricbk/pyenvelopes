from Envelope import Envelope
from envelope_manager_facade import EnvelopeManagerFacade

import datetime
from lxml import etree
from lxml.builder import E
import logging
import os

__MAX_WEEKLY_ENVELOPES = 4

def __tryInt(s):
    try:
        return int(s)
    except Exception:
        return None

def __tryParseWeeklyEnvelope(envelope):
    name_parts = envelope.name.split('_')
    if len(name_parts) != 3:
        return (None, None)
    if name_parts[0] != 'Week':
        return (None, None)

    year = __tryInt(name_parts[1])
    week = __tryInt(name_parts[2])

    return (year, week)

def filterWeeklyEnvelopes(envelopes):
    result = {}
    weeklyEnvelopeList = []
    for envelope in envelopes.values():
        year, week = __tryParseWeeklyEnvelope(envelope)
        if year is None or week is None:
           result[envelope.id] = envelope
        else:
          weeklyEnvelopeList.append((year, week, envelope))
    weeklyEnvelopeList.sort(reverse=True)
    for _, _, envelope in weeklyEnvelopeList[:__MAX_WEEKLY_ENVELOPES]:
        result[envelope.id] = envelope
    return result

class EnvelopeManager:
    __envelopeFileName = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        'envelopes.xml'
    )
    __instance = None

    @classmethod
    def instance(cls):
        if EnvelopeManager.__instance is None:
            EnvelopeManager.__instance = EnvelopeManager()
        return EnvelopeManager.__instance

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
        return filterWeeklyEnvelopes(self.__envelopes)

    def markEnvelopeAsArchive(self, envId):
        pass

    def idForEnvName(self, envName) -> int:
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
    def weekEnvelopeName(isoDate):
        year = isoDate[0]
        weekNum = isoDate[1]
        return "Week_{0}_{1}".format(year, weekNum)

    @property
    def currentEnvelope(self):
        isoDate = datetime.datetime.now().isocalendar()
        envName = self.weekEnvelopeName(isoDate)
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)

    @property
    def lastWeekEnvelope(self):
        isoDate = (datetime.datetime.now() - datetime.timedelta(days=7)).isocalendar()
        envName = self.weekEnvelopeName(isoDate)
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

class EnvelopeManagerFacadeImpl(EnvelopeManagerFacade):
    manager: EnvelopeManager

    def __init__(self, manager: EnvelopeManager):
        self.manager = manager

    def current_envelope_name(self):
        return self.manager.currentEnvelope.name

    def get_id_for_name(self, name: str) -> int:
        return self.manager.idForEnvName(name)

def make_facade(manager: EnvelopeManager) -> EnvelopeManagerFacade:
    return EnvelopeManagerFacadeImpl(manager)
