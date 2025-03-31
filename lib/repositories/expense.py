import shutil
import typing as ty
import uuid

import dateutil.parser
from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import ElementTree, _Element

from lib.models.expense import Expense
from lib.utils import unwrap


def expense_to_xml(expense: Expense) -> _Element:
    """Converts an Expense object to an XML element."""
    return E.Expense(
        id=str(expense.id),
        date=str(expense.date),
        value=str(expense.value),
        desc=expense.desc,
        fromId=str(expense.from_id),
        toId=str(expense.to_id),
        line=expense.line,
        manual=str(expense.manual),
    )


def xml_to_expense(el: _Element) -> Expense:
    """Converts an XML element to an Expense object."""
    return Expense(
        float(unwrap(el.get("value"))),
        unwrap(el.get("desc")),
        int(unwrap(el.get("fromId"))),
        int(unwrap(el.get("toId"))),
        unwrap(el.get("line")),
        unwrap(el.get("manual")) == "True",
        dateutil.parser.parse(unwrap(el.get("date"))),
        uuid.UUID(unwrap(el.get("id"))),
    )


class ExpenseRepository:
    _expenses: list[Expense] = []

    def __init__(self, fname: str) -> None:
        self._fname = fname
        self._load()

    @property
    def expenses(self) -> list[Expense]:
        return self._expenses

    def add_expense(self, expense: Expense) -> None:
        self._expenses.append(expense)
        self._save()

    # FIXME: replace usages with `add_expense(Expense)`
    def add_expense_for_rule(
        self,
        amount: float,
        from_id: int,
        to_id: int,
        comment: str = "Automatic expense",
    ) -> Expense:
        ex = Expense(amount, comment, from_id, to_id)
        self._expenses.append(ex)
        self._save()
        return ex

    def delete_expense(self, expense: Expense) -> None:
        self.expenses.remove(expense)
        self._save()

    def _load(self) -> None:
        try:
            doc = etree.parse(self._fname)
        except Exception as e:
            print(e)
            return

        for el in ty.cast(list[_Element], doc.xpath("//Expense")):
            try:
                self._expenses.append(xml_to_expense(el))
            except Exception as e:
                print(e)

    def _save(self) -> None:
        doc = E.Expenses()
        doc.extend([expense_to_xml(ex) for ex in self._expenses])
        tmp_file_name = self._fname + ".temp"
        ElementTree(doc).write(tmp_file_name, encoding="utf-8", pretty_print=True)
        shutil.move(tmp_file_name, self._fname)
