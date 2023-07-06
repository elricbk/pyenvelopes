from lxml import etree

from lib.models.envelope import Envelope


def test_to_xml__always__serializes_envelope() -> None:
    envelope = Envelope(id=42, name="42", desc="the number")

    result = envelope.toXml()

    assert result.attrib["id"] == "42"
    assert result.attrib["name"] == envelope.name
    assert result.attrib["desc"] == envelope.desc


def test_from_xml__given_serialized_envelope__loads_it() -> None:
    data = '<Envelope id="4" name="Week_2020_11" desc=""/>'

    result = Envelope.fromXml(etree.fromstring(data))

    assert result.id == 4
    assert result.name == "Week_2020_11"
