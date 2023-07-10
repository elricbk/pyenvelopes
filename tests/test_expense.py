import datetime
import uuid

from lxml import etree

from lib.models.expense import Expense


def test_ctor__given_no_id__generates_some() -> None:
    expense = Expense(42, "", 0, 0)

    assert isinstance(expense.id, uuid.UUID)


def test_ctor__given_no_date__sets_it_to_now() -> None:
    expense = Expense(42, "", 0, 0)

    assert datetime.datetime.now() - expense.date < datetime.timedelta(
        seconds=10.0
    )


def test_to_xml__always__serializes_expense() -> None:
    expense = Expense(42, "", 0, 0)

    result = expense.to_xml()

    assert result.attrib["id"] == str(expense.id)
    assert result.attrib["manual"] == "False"


def test_from_xml__given_serialized_expense__loads_it() -> None:
    data = """<Expense
        id="18844fd6-358b-4d82-8eaf-dcf536771e81"
        date="2020-03-09 13:35:00"
        value="42.0"
        desc="Automatic creation of weekly envelope"
        fromId="3"
        toId="4"
        line=""
        manual="False"
    />"""

    expense = Expense.from_xml(etree.fromstring(data))

    assert int(expense.value) == 42
    assert expense.from_id == 3
    assert expense.to_id == 4


def test_expense__always__can_be_used_as_map_key() -> None:
    expense = Expense(42, "", 0, 0)
    data = {}

    data[expense] = 4
