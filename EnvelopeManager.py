from Envelope import Envelope
import datetime
import os.path
from lxml import etree
from lxml.builder import E

class EnvelopeManager:
    __envelopeFileName = 'envelopes.xml'
    __instance = None

    @classmethod
    def instance(cls):
        if (EnvelopeManager.__instance == None):
            EnvelopeManager.__instance = EnvelopeManager()
        return __instance

    def __init__(self):
       self.__envelopes = { 1: Envelope.Income(), 2: Envelope.Expense(), 3: Envelope.Leftover() }
       self.__expMgr = None
       self.__loadSavedEnvelopes()

    def __maxId(self):
        return max(self.__envelopes.keys())

    def setExpenseManager(self, expMgr):
        self.__expMgr = expMgr

    def addEnvelope(self, name, desc=''):
        #print(u"Adding envelope with name {0}, id will be {1}".format(name, self.__maxId()))
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
        for k, v in self.__envelopes.items():
            if envName == v.name:
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

    @property
    def currentEnvelope(self):
        weekNum = datetime.datetime.now().isocalendar()[1]
        envName = "Week_{0}".format(weekNum)
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)

    def envelopeForDate(self, date):
        weekNum = date.isodate()[1]
        envName = "Week_{0}".format(weekNum)
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)
        
