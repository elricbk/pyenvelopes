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


class ExpenseManager:
    __expenseFileName = os.path.join(settings.data_path, "expenses.xml")

    __expenses: list[Expense] = []
    __envMgr: ty.Optional[EnvelopeManagerFacade] = None

    def __init__(self) -> None:
        self.__loadSavedExpenses()

    @property
    def expenses(self) -> list[Expense]:
        return self.__expenses

    def setEnvelopeManager(self, envMgr: EnvelopeManagerFacade) -> None:
        self.__envMgr = envMgr

    def addExpense(self, user_input: str) -> Expense:
        expense = parse_expense(user_input)
        envMgr = unwrap(self.__envMgr)
        if expense.from_envelope is None:
            expense.from_envelope = envMgr.current_envelope_name()
        ex = Expense(
            float(expense.amount),
            expense.comment,
            envMgr.get_id_for_name(expense.from_envelope),
            envMgr.get_id_for_name(expense.to_envelope),
            user_input,
            True,
        )
        self.__expenses.append(ex)
        self.__saveAllExpenses()
        return ex

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
