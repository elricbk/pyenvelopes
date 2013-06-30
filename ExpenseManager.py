# -*- coding: utf8 -*-
from Expense import Expense
import datetime
import re
import uuid
from lxml.etree import ElementTree
from lxml import etree
from lxml.builder import E
import logging

class ExpenseManager:
    __expenseFileName = 'data/expenses.xml'
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
        self.__saveAllExpenses()
        self.__expenses.append(ex)
        return ex

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
        ElementTree(doc).write(fname, encoding="utf-8", pretty_print=True)

    def __parseExpense(self, line):
        line = line.strip()
        rgxShort = '(\d+)\s+(\w.*)'
        rgxEnvelope = '(\d+)\s+(\w.*)\s+(\%\w+)'
        rgxFull = '(\d+)\s+(\w.*)\s+(\%\w+)\s+(\%\w+)'

        res = re.match(rgxFull, line, re.U)
        if res:
            return [res.group(1), res.group(2), res.group(3), res.group(4)]

        res = re.match(rgxEnvelope, line, re.U)
        if res:
            return [res.group(1), res.group(2), res.group(3), u'%корзина']

        res = re.match(rgxShort, line, re.U)
        if res:
            return [res.group(1), res.group(2), '#' + self.__envMgr.currentEnvelope.name, u'%корзина']
            
        raise Exception('Wrong format')
