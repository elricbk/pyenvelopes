from ExpenseRule import ExpenseRule
import uuid
from lxml import etree
from lxml.builder import E
import logging


class ExpenseRuleManager:
    __ruleFileName = 'data/rules.xml'
    __instance = None

    @classmethod
    def instance(cls):
        if ExpenseRuleManager.__instance is None:
            ExpenseRuleManager.__instance = ExpenseRuleManager()
        return ExpenseRuleManager.instance

    def __init__(self):
        self.__rules = []
        self.__loadSavedRules()

    def setExpenseManager(self, expMgr):
        self.__expMgr = expMgr

    @property
    def rules(self):
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





