from .envelope_manager_facade import EnvelopeManagerFacade
from .expense import Expense
from .parse_expense import parse_expense

from lxml import etree
from lxml.builder import E
from lxml.etree import ElementTree
from typing import List, Optional

import datetime
import logging
import os
import re
import shutil
import uuid

class ExpenseManager:
    __expenseFileName = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        'expenses.xml'
    )

    __expenses: List[Expense] = []
    __envMgr: EnvelopeManagerFacade = None

    def __init__(self):
        self.__loadSavedExpenses()

    @property
    def expenses(self) -> List[Expense]:
        return self.__expenses

    def setEnvelopeManager(self, envMgr: EnvelopeManagerFacade):
        self.__envMgr = envMgr

    def addExpense(self, user_input: str) -> Expense:
        expense = parse_expense(user_input)
        if expense.from_envelope is None:
            expense.from_envelope = self.__envMgr.current_envelope_name()
        ex = Expense(
            float(expense.amount),
            expense.comment,
            self.__envMgr.get_id_for_name(expense.from_envelope),
            self.__envMgr.get_id_for_name(expense.to_envelope),
            user_input,
            True
        )
        self.__expenses.append(ex)
        self.__saveAllExpenses()
        return ex

    def addExpenseForRule(
        self,
        amount: float,
        fromId: int,
        toId: int,
        comment: str='Automatic expense'
    ) -> Expense:
        ex = Expense(amount, comment, fromId, toId)
        self.__expenses.append(ex)
        self.__saveAllExpenses()
        return ex

    def deleteExpense(self, expense):
        self.expenses.remove(expense)
        self.__saveAllExpenses()

    def __loadSavedExpenses(self):
        try:
            doc = etree.parse(ExpenseManager.__expenseFileName)
        except Exception as e:
            print(e)
            return

        for el in doc.xpath("//Expense"):
            try:
                self.__expenses.append(Expense.fromXml(el))
            except Exception as e:
                print(e)

    def __saveAllExpenses(self):
        doc = E.Expenses()
        doc.extend([ex.toXml() for ex in self.__expenses])
        fname = ExpenseManager.__expenseFileName
        tmpFileName = fname + '.temp'
        ElementTree(doc).write(tmpFileName, encoding="utf-8", pretty_print=True)
        shutil.move(tmpFileName, fname)
