import logging
import os
import typing as ty
import uuid

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib import settings

from .ExpenseManager import ExpenseManager
from .ExpenseRule import ExpenseRule


class ExpenseRuleManager:
    __ruleFileName = os.path.join(settings.data_path, "rules.xml")
    __instance = None

    __expMgr: ExpenseManager
    __rules: list[ExpenseRule]

    def __init__(self) -> None:
        self.__rules = []
        self.__loadSavedRules()

    def setExpenseManager(self, expMgr: ExpenseManager) -> None:
        self.__expMgr = expMgr

    @property
    def rules(self) -> list[ExpenseRule]:
        return self.__rules

    def __loadSavedRules(self) -> None:
        try:
            doc = etree.parse(ExpenseRuleManager.__ruleFileName)
        except Exception:
            logging.exception("Exception while reading ExpenseRule datafile")
            return

        for el in ty.cast(list[_Element], doc.xpath("//ExpenseRule")):
            try:
                self.__rules.append(ExpenseRule.fromXml(el))
            except Exception:
                logging.exception("Exception while parsing ExpenseRule")

    def addRule(self, amount: float, fromId: int, toId: int) -> ExpenseRule:
        rule = ExpenseRule(uuid.uuid4(), amount, fromId, toId)
        self.__rules.append(rule)
        self.__saveAllRules()
        return rule

    def deleteRule(self, ruleId: uuid.UUID) -> None:
        rule = self.__getRuleById(ruleId)
        if rule is not None:
            self.__rules.remove(rule)
            self.__saveAllRules()

    def __getRuleById(self, ruleId: uuid.UUID) -> ty.Optional[ExpenseRule]:
        for rule in self.__rules:
            if rule.id == ruleId:
                return rule
        return None

    def clearAllRules(self) -> None:
        self.__rules = []

    def __saveAllRules(self) -> None:
        doc = E.ExpenseRules()
        doc.extend([rule.toXml() for rule in self.__rules])
        fname = ExpenseRuleManager.__ruleFileName
        etree.ElementTree(doc).write(fname, encoding="utf-8", pretty_print=True)

    def executeRule(self, ruleId: uuid.UUID) -> None:
        rule = self.__getRuleById(ruleId)
        if rule is not None:
            self.__expMgr.addExpenseForRule(rule.amount, rule.fromId, rule.toId)

    def executeAllRules(self) -> None:
        for rule in self.__rules:
            self.__expMgr.addExpenseForRule(rule.amount, rule.fromId, rule.toId)
