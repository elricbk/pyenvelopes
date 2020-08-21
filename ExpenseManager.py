# -*- coding: utf8 -*-
from Expense import Expense
from parse_expense import parse_expense

import datetime
import re
import uuid
from lxml.etree import ElementTree
from lxml import etree
from lxml.builder import E
import logging
import shutil
import os

class ExpenseManager:
    __expenseFileName = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        'expenses.xml'
    )
    __instance = None
    
    @classmethod
    def instance(cls):
        if ExpenseManager.__instance is None:
            ExpenseManager.__instance = ExpenseManager()
        return ExpenseManager.__instance

    def __init__(self):
        self.__expenses = []
        self.__envMgr = None
        self.__loadSavedExpenses()

    @property
    def expenses(self): 
        return self.__expenses

    def setEnvelopeManager(self, envMgr):
        self.__envMgr = envMgr

    def addExpense(self, userInput):
        ex = self.__fromUserInput(userInput)
        self.__expenses.append(ex)
        self.__saveAllExpenses()
        return ex

    def addExpenseForRule(self, amount, fromId, toId, comment='Automatic expense'):
        data = [
            uuid.uuid4(),
            datetime.datetime.now(),
            amount,
            comment,
            fromId,
            toId,
            '',
            False,
        ]
        ex = Expense(data)
        self.__expenses.append(ex)
        self.__saveAllExpenses()
        return ex

    def deleteExpense(self, expense):
        self.expenses.remove(expense)
        self.__saveAllExpenses()

    def __fromUserInput(self, line):
        parts = self.__parseExpense(line)
        data = [
            uuid.uuid4(),
            datetime.datetime.now(),
            parts[0],
            parts[1],
            self.__envMgr.idForEnvName(parts[2][1:]),
            self.__envMgr.idForEnvName(parts[3][1:]),
            line,
            True
        ]
        return Expense(data)

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

    def __parseExpense(self, line):
        expense = parse_expense(line)
        from_envelope = expense.from_envelope \
            if expense.from_envelope \
            else '%' + self.__envMgr.currentEnvelope.name
        return [
            expense.amount,
            expense.comment,
            from_envelope,
            expense.to_envelope
        ]
