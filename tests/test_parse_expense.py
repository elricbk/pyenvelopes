import unittest

import pytest

from lib.parse_expense import ParsedExpense, parse_expense
from lib.well_known_envelope import WellKnownEnvelope


def test_parse_expense__given_full_form_line__parses_it() -> None:
    line = "42 moving money %корзина %доход"
    expected_expense = ParsedExpense("42", "moving money", "корзина", "доход")

    result = parse_expense(line)

    assert result == expected_expense


def test_parse_expense__given_expense_from_envelope__parses_it() -> None:
    line = "24 spending money %запас"
    expected_expense = ParsedExpense(
        "24", "spending money", "запас", WellKnownEnvelope.TrashBin
    )

    result = parse_expense(line)

    assert result == expected_expense


def test_parse_expense__given_income_to_envelope__parses_it() -> None:
    line = "+84 getting money %envelope"
    expected_expense = ParsedExpense(
        "84", "getting money", WellKnownEnvelope.Income, "envelope"
    )

    result = parse_expense(line)

    assert result == expected_expense


def test_parse_expense__given_short_form__parses_it() -> None:
    line = "42 short form"
    expected_expense = ParsedExpense(
        "42",
        "short form",
        WellKnownEnvelope.ThisWeek,
        WellKnownEnvelope.TrashBin,
    )

    result = parse_expense(line)

    assert result == expected_expense


def test_parse_expense__given_unknown_line__throws() -> None:
    with pytest.raises(Exception):
        parse_expense("wrong format line")
