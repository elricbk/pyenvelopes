# -*- coding: utf8 -*-
import datetime
import re
import uuid
import shutil

from lxml.etree import ElementTree
from lxml import etree
from lxml.builder import E

from Expense import Expense


class ExpenseManager:
    __expenseFileName = 'data/expenses.xml'

    def __init__(self):
        self.__expenses = []
        self.__envMgr = None
        self.__loadSavedExpenses()

    @property
    def expenses(self): 
        return self.__expenses

    def setEnvelopeManager(self, envMgr):
        self.__envMgr = envMgr

    def addExpense(self, amount, fromId, toId, comment='Automatic expense', line='', manual=False):
        data = [
            uuid.uuid4(),
            datetime.datetime.now(),
            amount,
            comment,
            fromId,
            toId,
            line,
            manual
        ]
        ex = Expense(data)
        self.__saveAllExpenses()
        self.__expenses.append(ex)
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
