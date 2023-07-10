import shutil
import typing as ty

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import ElementTree, _Element

from lib.models.expense import Expense


class ExpenseRepository:
    __expenses: list[Expense] = []

    def __init__(self, fname: str) -> None:
        self._fname = fname
        self.__loadSavedExpenses()

    @property
    def expenses(self) -> list[Expense]:
        return self.__expenses

    def add_expense(self, expense: Expense) -> None:
        self.__expenses.append(expense)
        self.__saveAllExpenses()

    def addExpenseForRule(
        self,
        amount: float,
        fromId: int,
        toId: int,
        comment: str = "Automatic expense",
    ) -> Expense:
        ex = Expense(amount, comment, fromId, toId)
        self.__expenses.append(ex)
        self.__saveAllExpenses()
        return ex

    def deleteExpense(self, expense: Expense) -> None:
        self.expenses.remove(expense)
        self.__saveAllExpenses()

    def __loadSavedExpenses(self) -> None:
        try:
            doc = etree.parse(self._fname)
        except Exception as e:
            print(e)
            return

        for el in ty.cast(list[_Element], doc.xpath("//Expense")):
            try:
                self.__expenses.append(Expense.from_xml(el))
            except Exception as e:
                print(e)

    def __saveAllExpenses(self) -> None:
        doc = E.Expenses()
        doc.extend([ex.to_xml() for ex in self.__expenses])
        fname = self._fname
        tmpFileName = fname + ".temp"
        ElementTree(doc).write(tmpFileName, encoding="utf-8", pretty_print=True)
        shutil.move(tmpFileName, fname)
