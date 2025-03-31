import uuid
from lxml import etree

from lib.models.expense_rule import ExpenseRule
from lib.repositories.expense_rule import expense_rule_to_xml, xml_to_expense_rule


def test_to_xml__always__serializes_expense_rule() -> None:
    rule = ExpenseRule(uuid.uuid4(), 42.0, 1, 2)
    result = expense_rule_to_xml(rule)
    assert result.attrib["id"] == str(rule.id)
    assert result.attrib["amount"] == str(rule.amount)
    assert result.attrib["fromId"] == str(rule.from_id)
    assert result.attrib["toId"] == str(rule.to_id)


def test_from_xml__given_serialized_expense_rule__loads_it() -> None:
    data = """<ExpenseRule
        id="18844fd6-358b-4d82-8eaf-dcf536771e81"
        amount="42.0"
        fromId="1"
        toId="2"
    />"""
    rule = xml_to_expense_rule(etree.fromstring(data))
    assert rule.id == uuid.UUID("18844fd6-358b-4d82-8eaf-dcf536771e81")
    assert rule.amount == 42.0
    assert rule.from_id == 1
    assert rule.to_id == 2