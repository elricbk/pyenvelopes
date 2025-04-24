import uuid
from lxml import etree

from lib.models.business_plan_item import BusinessPlanItem, ItemType, Frequency
from lib.repositories.business_plan.xml.business_plan import business_plan_item_to_xml, xml_to_business_plan_item


def test_to_xml__always__serializes_expense_rule() -> None:
    item = BusinessPlanItem(uuid.uuid4(), ItemType.Income, 42., "test", Frequency.Weekly)
    result = business_plan_item_to_xml(item)
    assert result.attrib["id"] == str(item.id)
    assert result.attrib["type"] == str(item.type.value)
    assert result.attrib["amount"] == str(item.amount)
    assert result.attrib["name"] == str(item.name)
    assert result.attrib["freq"] == str(item.freq.value)


def test_from_xml__given_serialized_expense_rule__loads_it() -> None:
    data = """<Item
        id="6e8d2c37-0322-4d0b-a13f-8d86df05c874"
        type="2"
        amount="10000.0"
        name="квартплата"
        freq="4"
    />"""
    rule = xml_to_business_plan_item(etree.fromstring(data))
    assert rule.id == uuid.UUID("6e8d2c37-0322-4d0b-a13f-8d86df05c874")
    assert rule.amount == 10000.0
    assert rule.type == ItemType.Expense
    assert rule.freq == Frequency.Monthly