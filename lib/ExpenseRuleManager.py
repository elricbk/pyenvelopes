from .ExpenseRule import ExpenseRule
from .ExpenseManager import ExpenseManager

import uuid
from lxml import etree
from lxml.builder import E # type: ignore
from typing import List
import logging
import os
import settings


class ExpenseRuleManager:
    __ruleFileName = os.path.join(settings.data_path, 'rules.xml')
    __instance = None

    __expMgr: ExpenseManager
    __rules: List[ExpenseRule]

    def __init__(self):
        self.__rules = []
        self.__loadSavedRules()

    def setExpenseManager(self, expMgr: ExpenseManager):
        self.__expMgr = expMgr

    @property
    def rules(self) -> List[ExpenseRule]:
        return self.__rules

    def __loadSavedRules(self):
        try:
            doc = etree.parse(ExpenseRuleManager.__ruleFileName)
        except Exception:
            logging.exception("Exception while reading ExpenseRule datafile")
            return

        for el in doc.xpath("//ExpenseRule"):
            try:
                self.__rules.append(ExpenseRule.fromXml(el))
            except Exception:
                logging.exception("Exception while parsing ExpenseRule")

    def addRule(self, amount, fromId, toId):
        rule = ExpenseRule(uuid.uuid4(), amount, fromId, toId)
        self.__rules.append(rule)
        self.__saveAllRules()
        return rule

    def deleteRule(self, ruleId):
        rule = self.__getRuleById(ruleId)
        if rule is not None:
            self.__rules.remove(rule)
            self.__saveAllRules()

    def __getRuleById(self, ruleId):
        for rule in self.__rules:
            if rule.id == ruleId:
                return rule
        return None

    def clearAllRules(self):
        self.__rules = []

    def __saveAllRules(self):
        doc = E.ExpenseRules()
        doc.extend([rule.toXml() for rule in self.__rules])
        fname = ExpenseRuleManager.__ruleFileName
        etree.ElementTree(doc).write(fname, encoding="utf-8", pretty_print=True)

    def executeRule(self, ruleId):
        rule = self.__getRuleById(ruleId)
        if rule is not None:
            self.__expMgr.addExpenseForRule(rule.amount, rule.fromId, rule.toId)

    def executeAllRules(self):
        for rule in self.__rules:
            self.__expMgr.addExpenseForRule(rule.amount, rule.fromId, rule.toId)





