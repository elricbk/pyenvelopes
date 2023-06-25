import unittest

import pytest
from lib.parse_expense import parse_expense


def test_parse_expense__given_full_form_line__parses_it() -> None:
    line = "42 moving money %корзина %доход"

    result = parse_expense(line)

    assert result.amount == "42"
    assert result.comment == "moving money"
    assert result.from_envelope == "корзина"
    assert result.to_envelope == "доход"


def test_parse_expense__given_expense_from_envelope__parses_it() -> None:
    line = "24 spending money %запас"

    result = parse_expense(line)

    assert result.amount == "24"
    assert result.comment == "spending money"
    assert result.from_envelope == "запас"
    assert result.to_envelope == "корзина"


def test_parse_expense__given_income_to_envelope__parses_it() -> None:
    line = "+84 getting money %envelope"

    result = parse_expense(line)

    assert result.amount == "84"
    assert result.comment == "getting money"
    assert result.from_envelope == "доход"
    assert result.to_envelope == "envelope"


def test_parse_expense__given_short_form__parses_it() -> None:
    line = "42 short form"

    result = parse_expense(line)

    assert result.amount == "42"
    assert result.comment == "short form"
    assert result.from_envelope is None
    assert result.to_envelope == "корзина"


def test_parse_expense__given_unknown_line__throws() -> None:
    with pytest.raises(Exception):
        parse_expense("wrong format line")
