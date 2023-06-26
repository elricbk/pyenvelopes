import datetime
import logging
import os
import re
import shutil
import typing as ty
import uuid

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import ElementTree, _Element

from lib import settings
from lib.utils import unwrap

from .envelope_manager_facade import EnvelopeManagerFacade
from .expense import Expense
from .parse_expense import parse_expense
from .well_known_envelope import WellKnownEnvelope


class ExpenseManager:
    __expenseFileName = os.path.join(settings.data_path, "expenses.xml")

    __expenses: list[Expense] = []

    def __init__(self) -> None:
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
            doc = etree.parse(ExpenseManager.__expenseFileName)
        except Exception as e:
            print(e)
            return

        for el in ty.cast(list[_Element], doc.xpath("//Expense")):
            try:
                self.__expenses.append(Expense.fromXml(el))
            except Exception as e:
                print(e)

    def __saveAllExpenses(self) -> None:
        doc = E.Expenses()
        doc.extend([ex.toXml() for ex in self.__expenses])
        fname = ExpenseManager.__expenseFileName
        tmpFileName = fname + ".temp"
        ElementTree(doc).write(tmpFileName, encoding="utf-8", pretty_print=True)
        shutil.move(tmpFileName, fname)
