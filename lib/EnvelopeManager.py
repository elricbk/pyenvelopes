import datetime
import logging
import os
import typing as ty
from typing import Dict

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib import settings
from lib.utils import unwrap

from .Envelope import Envelope, EnvelopeId
from .ExpenseManager import ExpenseManager
from .well_known_envelope import WellKnownEnvelope

__MAX_WEEKLY_ENVELOPES = 4


def __tryInt(s: str) -> ty.Optional[int]:
    try:
        return int(s)
    except Exception:
        return None


def __tryParseWeeklyEnvelope(
    envelope: Envelope,
) -> tuple[ty.Optional[int], ty.Optional[int]]:
    name_parts = envelope.name.split("_")
    if len(name_parts) != 3:
        return (None, None)
    if name_parts[0] != "Week":
        return (None, None)

    year = __tryInt(name_parts[1])
    week = __tryInt(name_parts[2])

    return (year, week)


def filterWeeklyEnvelopes(
    envelopes: dict[EnvelopeId, Envelope],
) -> dict[EnvelopeId, Envelope]:
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
    __envelopeFileName = os.path.join(settings.data_path, "envelopes.xml")

    __envelopes: Dict[EnvelopeId, Envelope] = {
        WellKnownEnvelope.Income.value: Envelope(1, "Income", ""),
        WellKnownEnvelope.TrashBin.value: Envelope(2, "Expense", ""),
        WellKnownEnvelope.Leftover.value: Envelope(3, "Leftover", ""),
    }

    def __init__(self) -> None:
        self.__expMgr: ty.Optional[ExpenseManager] = None
        self.__loadSavedEnvelopes()

    def __maxId(self) -> EnvelopeId:
        return max(self.__envelopes.keys())

    def setExpenseManager(self, expMgr: ExpenseManager) -> None:
        self.__expMgr = expMgr

    def addEnvelope(self, name: str, desc: str = "") -> Envelope:
        logging.info(
            "Adding envelope with name %s, id will be %d", name, self.__maxId()
        )
        # FIXME: disallow creation of envelopes with spaces
        if name.lower() in (v.name.lower() for v in self.envelopes.values()):
            raise RuntimeError("Envelope with given name already exists")
        e = Envelope(self.__maxId() + 1, name, desc)
        self.__envelopes[e.id] = e
        self.__saveAllEnvelopes()
        return e

    def __saveAllEnvelopes(self) -> None:
        doc = E.Envelopes()
        doc.extend([env.toXml() for env in self.__envelopes.values()])
        etree.ElementTree(doc).write(
            EnvelopeManager.__envelopeFileName,
            pretty_print=True,
            encoding="utf-8",
        )

    def __loadSavedEnvelopes(self) -> None:
        try:
            doc = etree.parse(EnvelopeManager.__envelopeFileName)
        except Exception as e:
            print(e)
            return

        for el in ty.cast(list[_Element], doc.xpath("//Envelope")):
            try:
                env = Envelope.fromXml(el)
                self.__envelopes[env.id] = env
            except Exception as e:
                print(e)

    @property
    def envelopes(self) -> dict[EnvelopeId, Envelope]:
        return filterWeeklyEnvelopes(self.__envelopes)

    def markEnvelopeAsArchive(self, envId: EnvelopeId) -> None:
        # FIXME: implement archive envelopes
        pass

    def idForEnvName(self, envName: str) -> EnvelopeId:
        # print(u"Searching for envelope '{0}'".format(envName))
        # FIXME: envelope name is not unique, it may lead to problems
        for k, v in self.__envelopes.items():
            if envName.lower() == v.name.lower():
                return k
        raise Exception(
            f'No envelope with name "{envName}", known envelopes: {self.__envelopes}'
        )

    def envNameForId(self, envId: EnvelopeId) -> str:
        return self.__envelopes[envId].name

    def envelopeValue(self, envId: EnvelopeId) -> float:
        value = 0.0
        for ex in unwrap(self.__expMgr).expenses:
            if ex.fromId == envId:
                value -= ex.value
            if ex.toId == envId:
                value += ex.value
        return value

    @staticmethod
    def weekEnvelopeName(isoDate: tuple) -> str:
        year = isoDate[0]
        weekNum = isoDate[1]
        return f"Week_{year}_{weekNum}"

    @property
    def currentEnvelope(self) -> Envelope:
        isoDate = datetime.datetime.now().isocalendar()
        envName = self.weekEnvelopeName(isoDate)
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)

    @property
    def lastWeekEnvelope(self) -> Envelope:
        isoDate = (
            datetime.datetime.now() - datetime.timedelta(days=7)
        ).isocalendar()
        envName = self.weekEnvelopeName(isoDate)
        for k, v in self.__envelopes.items():
            if envName == v.name:
                return v

        return self.addEnvelope(envName)
