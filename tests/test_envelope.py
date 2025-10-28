from lxml import etree

from lib.models.envelope import Envelope
from lib.repositories.envelope.xml.envelope import (
    envelope_to_xml,
    xml_to_envelope,
)


def test_to_xml__always__serializes_envelope() -> None:
    envelope = Envelope(id=42, name="42", desc="the number")

    result = envelope_to_xml(envelope)

    assert result.attrib["id"] == "42"
    assert result.attrib["name"] == envelope.name
    assert result.attrib["desc"] == envelope.desc
    assert result.attrib["archived"] == "false"


def test_to_xml__archived_envelope__serializes_archived_flag() -> None:
    envelope = Envelope(id=42, name="42", desc="the number", archived=True)

    result = envelope_to_xml(envelope)

    assert result.attrib["archived"] == "true"


def test_from_xml__given_serialized_envelope__loads_it() -> None:
    data = '<Envelope id="4" name="Week_2020_11" desc=""/>'

    result = xml_to_envelope(etree.fromstring(data))

    assert result.id == 4
    assert result.name == "Week_2020_11"
    assert result.archived is False


def test_from_xml__given_archived_envelope__loads_archived_flag() -> None:
    data = '<Envelope id="4" name="Week_2020_11" desc="" archived="true"/>'

    result = xml_to_envelope(etree.fromstring(data))

    assert result.id == 4
    assert result.name == "Week_2020_11"
    assert result.archived is True


def test_from_xml__missing_archived_attribute__defaults_to_false() -> None:
    data = '<Envelope id="4" name="Week_2020_11" desc=""/>'

    result = xml_to_envelope(etree.fromstring(data))

    assert result.archived is False
