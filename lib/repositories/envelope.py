import datetime
import logging
import typing as ty

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element
from lxml.builder import E  # type: ignore

from lib.models.envelope import Envelope, EnvelopeId
from lib.utils import unwrap
from lib.well_known_envelope import WellKnownEnvelope

from .expense import ExpenseRepository


def envelope_to_xml(envelope: Envelope) -> _Element:
    """Converts an Envelope object to an XML element."""
    return E.Envelope(id=str(envelope.id), name=envelope.name, desc=envelope.desc)


def xml_to_envelope(el: _Element) -> Envelope:
    """Converts an XML element to an Envelope object."""
    return Envelope(
        int(unwrap(el.get("id"))),
        unwrap(el.get("name")),
        unwrap(el.get("desc")),
    )


__MAX_WEEKLY_ENVELOPES = 4


def _try_parse_int(s: str) -> ty.Optional[int]:
    try:
        return int(s)
    except Exception:
        return None


def _try_parse_weekly_envelope(
    envelope: Envelope,
) -> tuple[ty.Optional[int], ty.Optional[int]]:
    name_parts = envelope.name.split("_")
    if len(name_parts) != 3:
        return (None, None)
    if name_parts[0] != "Week":
        return (None, None)

    year = _try_parse_int(name_parts[1])
    week = _try_parse_int(name_parts[2])

    return (year, week)


def _filter_weekly_envelopes(
    envelopes: dict[EnvelopeId, Envelope],
) -> dict[EnvelopeId, Envelope]:
    result = {}
    weekly_envelopes = []
    for envelope in envelopes.values():
        year, week = _try_parse_weekly_envelope(envelope)
        if year is None or week is None:
            result[envelope.id] = envelope
        else:
            weekly_envelopes.append((year, week, envelope))
    weekly_envelopes.sort(reverse=True)
    for _, _, envelope in weekly_envelopes[:__MAX_WEEKLY_ENVELOPES]:
        result[envelope.id] = envelope
    return result


def _week_envelope_name(iso_date: tuple) -> str:
    year = iso_date[0]
    week_number = iso_date[1]
    return f"Week_{year}_{week_number}"


class EnvelopeRepository:
    _envelopes: dict[EnvelopeId, Envelope] = {
        WellKnownEnvelope.Income.value: Envelope(1, "Income", ""),
        WellKnownEnvelope.TrashBin.value: Envelope(2, "Expense", ""),
        WellKnownEnvelope.Leftover.value: Envelope(3, "Leftover", ""),
    }

    def __init__(self, fname: str) -> None:
        self._expense_repository: ty.Optional[ExpenseRepository] = None
        self._fname = fname
        self._load()

    def _max_id(self) -> EnvelopeId:
        return max(self._envelopes.keys())

    def set_expense_repository(self, expenses: ExpenseRepository) -> None:
        self._expense_repository = expenses

    def add_envelope(self, name: str, desc: str = "") -> Envelope:
        logging.info(
            "Adding envelope with name %s, id will be %d", name, self._max_id()
        )
        # FIXME: disallow creation of envelopes with spaces
        if name.lower() in (v.name.lower() for v in self.envelopes.values()):
            raise RuntimeError("Envelope with given name already exists")
        e = Envelope(self._max_id() + 1, name, desc)
        self._envelopes[e.id] = e
        self._save()
        return e

    def _save(self) -> None:
        doc = E.Envelopes()
        doc.extend([envelope_to_xml(env) for env in self._envelopes.values()])
        etree.ElementTree(doc).write(
            self._fname, pretty_print=True, encoding="utf-8"
        )

    def _load(self) -> None:
        try:
            doc = etree.parse(self._fname)
        except Exception as e:
            print(e)
            return

        for el in ty.cast(list[_Element], doc.xpath("//Envelope")):
            try:
                env = xml_to_envelope(el)
                self._envelopes[env.id] = env
            except Exception as e:
                print(e)

    @property
    def envelopes(self) -> dict[EnvelopeId, Envelope]:
        return _filter_weekly_envelopes(self._envelopes)

    def id_for_envelope_name(self, name: str) -> EnvelopeId:
        # print(u"Searching for envelope '{0}'".format(envName))
        # FIXME: envelope name is not unique, it may lead to problems
        for k, v in self._envelopes.items():
            if name.lower() == v.name.lower():
                return k
        raise Exception(
            f'No envelope with name "{name}", '
            f"known envelopes: {self._envelopes}"
        )

    def envelope_name_for_id(self, id: EnvelopeId) -> str:
        return self._envelopes[id].name

    def envelope_value(self, id: EnvelopeId) -> float:
        value = 0.0
        for ex in unwrap(self._expense_repository).expenses:
            if ex.from_id == id:
                value -= ex.value
            if ex.to_id == id:
                value += ex.value
        return value

    @property
    def this_week_envelope(self) -> Envelope:
        iso_date = datetime.datetime.now().isocalendar()
        name = _week_envelope_name(iso_date)
        for k, v in self._envelopes.items():
            if name == v.name:
                return v

        return self.add_envelope(name)

    @property
    def last_week_envelope(self) -> Envelope:
        iso_date = (
            datetime.datetime.now() - datetime.timedelta(days=7)
        ).isocalendar()
        name = _week_envelope_name(iso_date)
        for k, v in self._envelopes.items():
            if name == v.name:
                return v

        return self.add_envelope(name)
