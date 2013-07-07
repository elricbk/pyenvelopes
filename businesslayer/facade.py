# coding=utf-8
"""
Facade for all business logic in the application, this class should be used from external code
"""

from ExpenseManager import ExpenseManager
from EnvelopeManager import EnvelopeManager
from ExpenseRuleManager import ExpenseRuleManager
from BusinessPlan import BusinessPlan
from RulesAppliedManager import RulesAppliedManager


class Facade(object):
    def __init__(self):
        self._setupManagers()

    def _setupManagers(self):
        self._expMgr = ExpenseManager()
        self._envMgr = EnvelopeManager()
        self._ruleMgr = ExpenseRuleManager()
        self._bp = BusinessPlan()
        self._rulesAppliedMgr = RulesAppliedManager()

        self._expMgr.setEnvelopeManager(self._envMgr)
        self._envMgr.setExpenseManager(self._expMgr)
        self._ruleMgr.setExpenseManager(self._expMgr)

    # region Expenses

    def addExpense(self, value, fromId, toId, desc="Automatic expense"):
        self._expMgr.addExpenseForRule(value, fromId, toId, desc)

    def deleteExpense(self, expense):
        self._expMgr.deleteExpense(expense)

    @property
    def expenses(self):
        return self._expMgr.expenses

    # endregion

    #region Envelopes

    @property
    def envelopes(self):
        return self._envMgr.envelopes

    def addEnvelope(self, name, description):
        self._envMgr.addEnvelope(name, description)

    def sealEnvelope(self, envId):
        self._envMgr.markEnvelopeAsArchive(envId)

    @property
    def currentEnvelope(self):
        return self._envMgr.currentEnvelope

    @property
    def lastWeekEnvelope(self):
        # FIXME: hack method, stuff it is needed for should be in this class, not in MainForm
        return self._envMgr.lastWeekEnvelope

    def envelopeValue(self, envId):
        self._envMgr.envelopeValue(envId)

    def envNameForId(self, envId):
        self._envMgr.envNameForId(envId)

    def idForEnvName(self, envName):
        self._envMgr.idForEnvName(envName)

    #endregion

    #region BusinessPlan

    @property
    def items(self):
        return self._bp.items

    def addItem(self, itemType, amount, name, freq):
        return self._bp.addItem(itemType, amount, name, freq)

    @property
    def weeklyIncome(self):
        return self._bp.weeklyIncome

    @property
    def weeklyExpense(self):
        return self._bp.weeklyExpense

    @property
    def weeklyEnvelope(self):
        return self._bp.weeklyEnvelope

    #endregion

    # region ExpenseRuleManager

    @property
    def rules(self):
        return self._ruleMgr.rules

    def addRule(self, amount, fromId, toId):
        self._ruleMgr.addRule(amount, fromId, toId)

    def deleteRule(self, ruleId):
        self._ruleMgr.deleteRule(ruleId)

    def clearAllRules(self):
        self._ruleMgr.clearAllRules()


    def executeRule(self, ruleId):
        self._ruleMgr.executeRule(ruleId)

    def executeAllRules(self):
        self._ruleMgr.executeAllRules()

    #endregion

    # region RulesAppliedManager

    def rulesAppliedForWeek(self, weekId):
        return self._rulesAppliedMgr.rulesAppliedForWeek(weekId)

    def markWeekAsRulesApplied(self, weekId):
        self._rulesAppliedMgr.markWeekAsRulesApplied(weekId)

    # endregion
