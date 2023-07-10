import logging
import typing as ty
import uuid

from lxml import etree
from lxml.builder import E  # type: ignore
from lxml.etree import _Element

from lib.models.expense_rule import ExpenseRule

from .expense import ExpenseRepository


class ExpenseRuleRepository:
    __instance = None

    __expMgr: ExpenseRepository
    __rules: list[ExpenseRule]

    def __init__(self, fname: str) -> None:
        self.__rules = []
        self._fname = fname
        self.__loadSavedRules()

    def setExpenseManager(self, expMgr: ExpenseRepository) -> None:
        self.__expMgr = expMgr

    @property
    def rules(self) -> list[ExpenseRule]:
        return self.__rules

    def __loadSavedRules(self) -> None:
        try:
            doc = etree.parse(self._fname)
        except Exception:
            logging.exception("Exception while reading ExpenseRule datafile")
            return

        for el in ty.cast(list[_Element], doc.xpath("//ExpenseRule")):
            try:
                self.__rules.append(ExpenseRule.from_xml(el))
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
        doc.extend([rule.to_xml() for rule in self.__rules])
        fname = self._fname
        etree.ElementTree(doc).write(fname, encoding="utf-8", pretty_print=True)

    def executeRule(self, ruleId: uuid.UUID) -> None:
        rule = self.__getRuleById(ruleId)
        if rule is not None:
            self.__expMgr.add_expense_for_rule(rule.amount, rule.from_id, rule.to_id)

    def executeAllRules(self) -> None:
        for rule in self.__rules:
            self.__expMgr.add_expense_for_rule(rule.amount, rule.from_id, rule.to_id)
