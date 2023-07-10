import shutil
import typing as ty

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import ElementTree, _Element

from lib.models.expense import Expense


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
                self._expenses.append(Expense.from_xml(el))
            except Exception as e:
                print(e)

    def _save(self) -> None:
        doc = E.Expenses()
        doc.extend([ex.to_xml() for ex in self._expenses])
        tmp_file_name = self._fname + ".temp"
        ElementTree(doc).write(tmp_file_name, encoding="utf-8", pretty_print=True)
        shutil.move(tmp_file_name, self._fname)
