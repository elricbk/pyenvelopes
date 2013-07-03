import logging
import datetime
from ui_MainForm import Ui_MainWindow
from PySide.QtGui import QMainWindow, QApplication
from ExpenseManager import ExpenseManager
from EnvelopeManager import EnvelopeManager
from ExpenseRuleManager import ExpenseRuleManager
from BusinessPlan import BusinessPlan
from BusinessPlanItem import Frequency, ItemType
from RulesAppliedManager import RulesAppliedManager
from PySide.QtGui import QTableWidgetItem, QMessageBox
from PySide.QtCore import Qt

DAYS_TO_SHOW_THRESHOLD = 14
# FIXME: this is hardcoded Leftover envelope ID, this should be done not this way
LeftoverEnvelopeId = 3


class MainForm(QMainWindow):
    def __init__(self, obj=None):
        super(MainForm, self).__init__(obj)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.setupExpenseTable()
        self.setupEnvelopeTable()
        self.setupRulesTable()
        self.setupPlanTable()
        self.setupManagers()
        self.loadExpenses()
        self.loadEnvelopes()
        self.loadRules()
        self.loadBusinessPlan()
        self.showCurrentEnvelopeValue()
        # FIXME: update completion model on new envelopes
        self.setupAutoCompletion()
        # FIXME: config or constant
        self.applyRulesAutomatically()
        self.startTimer(60 * 60 * 1000)

    def setupAutoCompletion(self):
        names = []
        for envelope in self.__envMgr.envelopes.values():
            # FIXME: this is a hack to remove weekly envelopes from autocompletion
            if envelope.name.startswith("Week_"):
                continue
            names.append("%" + envelope.name)
        self.__ui.leExpenseUserInput.setModel(names)

    def showCurrentEnvelopeValue(self):
        env = self.__envMgr.currentEnvelope
        value = self.__envMgr.envelopeValue(env.id)
        msg = "Current envelope ({0}): {1}".format(env.name, value)
        self.__ui.statusbar.showMessage(msg)

    def applyRulesAutomatically(self):
        if self.needToApplyRules():
            # FIXME: there should be transaction here -- all stuff should be done together or not at all
            self.createEnvelopeForNewWeek()
            self.transferAllFromLastWeek()
            self.__ruleMgr.executeAllRules()
            try:
                self.markWeekAsRulesApplied()
            except Exception:
                QMessageBox.critical(self, "Error marking this week as rules applied",
                                     "This error should be fixed manually")
                QApplication.quit()
            self.loadExpenses()

    def timerEvent(self, event):
        logging.debug("Timer event for timer: %d", event.timerId())
        self.applyRulesAutomatically()

    def markWeekAsRulesApplied(self):
        self.__rulesAppliedMgr.markWeekAsRulesApplied(self.__envMgr.currentEnvelope.name)

    def transferAllFromLastWeek(self):
        lwe = self.__envMgr.lastWeekEnvelope
        logging.debug("Transferring all money (%d) from last week (%s)", self.__envMgr.envelopeValue(lwe.id), lwe.name)
        self.__expMgr.addExpenseForRule(
            self.__envMgr.envelopeValue(lwe.id),
            lwe.id,
            self.__envMgr.currentEnvelope.id,
            "Automatic transfer of money from previous week"
        )

    def needToApplyRules(self):
        curEnvName = self.__envMgr.currentEnvelope.name
        logging.debug("Checking if need to apply rules for envelope %s", curEnvName)
        shouldApply = not self.__rulesAppliedMgr.rulesAppliedForWeek(curEnvName)
        logging.debug("Rules should be applied: %s", shouldApply)
        return shouldApply

    def createEnvelopeForNewWeek(self):
        logging.debug("Creating envelope for current week")
        self.__expMgr.addExpenseForRule(
            self.__bp.weeklyEnvelope,
            LeftoverEnvelopeId,
            self.__envMgr.currentEnvelope.id,
            "Automatic creation of weekly envelope"
        )

    def setupManagers(self):
        self.__expMgr = ExpenseManager()
        self.__envMgr = EnvelopeManager()
        self.__ruleMgr = ExpenseRuleManager()
        self.__bp = BusinessPlan()
        self.__rulesAppliedMgr = RulesAppliedManager()

        self.__expMgr.setEnvelopeManager(self.__envMgr)
        self.__envMgr.setExpenseManager(self.__expMgr)
        self.__ruleMgr.setExpenseManager(self.__expMgr)

    def setupExpenseTable(self):
        self.__ui.tableWidget.setHorizontalHeaderLabels(['Date', 'Value', 'From', 'To', 'Description'])
        self.__ui.tableWidget_3.setHorizontalHeaderLabels(['Date', 'Value', 'From', 'To', 'Description'])

    def setupEnvelopeTable(self):
        self.__ui.tableWidget_2.setHorizontalHeaderLabels(['Value', 'Envelope name'])

    def setupRulesTable(self):
        self.__ui.twRules.setHorizontalHeaderLabels(['Amount', 'From', 'To'])

    def setupPlanTable(self):
        self.__ui.twBusinessPlan.setHorizontalHeaderLabels(
            ['Type', 'Amount', 'Name', 'Description', 'Weekly', 'Envelope'])
        for i in range(ItemType.ItemsCount):
            self.__ui.cbItemType.addItem(ItemType.desc(i), i)
        self.__ui.cbItemType.setCurrentIndex(1)
        for i in range(Frequency.ItemsCount):
            self.__ui.cbItemFrequency.addItem(Frequency.desc(i), i)
        self.__ui.cbItemFrequency.setCurrentIndex(4)

    def addBusinessPlanItem(self):
        try:
            cbType = self.__ui.cbItemType
            cbFreq = self.__ui.cbItemFrequency
            parts = self.__ui.leNewBPItem.text().split(' ', 2)
            item = self.__bp.addItem(cbType.itemData(cbType.currentIndex()), int(parts[0]), parts[1],
                                     cbFreq.itemData(cbFreq.currentIndex()))
            self.addRowForPlanItem(item)
            self.__ui.leNewBPItem.setText('')
            self.showWeeklyStats()
        except Exception as e:
            print(e)

    def applyBusinessPlan(self):
        self.__bp.save()
        self.__ruleMgr.clearAllRules()
        for finItem in [i for i in self.__bp.items if i.type == ItemType.Expense]:
            try:
                envId = self.__envMgr.idForEnvName(finItem.name)
            except Exception as e:
                print(e)
                envId = self.__envMgr.addEnvelope(finItem.name).id
            self.__ruleMgr.addRule(finItem.weeklyValue, 3, envId)
        self.loadRules()
        bp = self.__bp
        QMessageBox.information(self, "Financial plan saved",
                                "Weekly income: {0}\nWeekly expense: {1}\nWeekly envelope: {2}".format(
                                    bp.weeklyIncome, bp.weeklyExpense, bp.weeklyEnvelope))

    def clearTable(self, tw):
        tw.clearContents()
        tw.setRowCount(0)

    def loadBusinessPlan(self):
        tw = self.__ui.twBusinessPlan
        self.clearTable(tw)
        for item in self.__bp.items:
            self.addRowForPlanItem(item)
        tw.resizeColumnsToContents()
        self.showWeeklyStats()

    def showWeeklyStats(self):
        info = "Weekly stats: Income = {0}, Expense = {1}, Envelope = {2}".format(
            self.__bp.weeklyIncome,
            self.__bp.weeklyExpense,
            self.__bp.weeklyEnvelope)
        self.__ui.lblWeeklyStats.setText(info)

    def addRowForPlanItem(self, item):
        tw = self.__ui.twBusinessPlan
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        tw.setItem(row, 0, self.itemWithId(ItemType.desc(item.type), item.id))
        tw.setItem(row, 1, self.itemWithId(str(item.amount), item.id))
        tw.setItem(row, 2, self.itemWithId(item.name, item.id))
        tw.setItem(row, 3, self.itemWithId(Frequency.desc(item.freq), item.id))
        tw.setItem(row, 4, self.itemWithId(str(item.weeklyValue), item.id))
        for env in self.__envMgr.envelopes.values():
            if env.name == item.name:
                tw.setItem(row, 5, self.itemWithId('Existing', item.id))
                return
        else:
            tw.setItem(row, 5, self.itemWithId('New', item.id))

    def loadRules(self):
        tw = self.__ui.twRules
        self.clearTable(tw)
        for rule in self.__ruleMgr.rules:
            self.addRowForRule(rule)
        tw.resizeColumnsToContents()

    def addRowForRule(self, rule):
        tw = self.__ui.twRules
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        tw.setItem(row, 0, self.itemWithId(str(rule.amount), rule.id))
        tw.setItem(row, 1, self.itemWithId(self.__envMgr.envNameForId(rule.fromId), rule.id))
        tw.setItem(row, 2, self.itemWithId(self.__envMgr.envNameForId(rule.toId), rule.id))

    def applyRules(self):
        self.__ruleMgr.executeAllRules()
        self.loadExpenses()

    def loadExpenses(self):
        self.clearTable(self.__ui.tableWidget)
        now = datetime.datetime.now()
        for ex in (e for e in self.__expMgr.expenses if (now - e.date).days < DAYS_TO_SHOW_THRESHOLD):
            self.addRowForExpense(self.__ui.tableWidget, ex)
        self.__ui.tableWidget.resizeColumnsToContents()
        # HACK: removes glitch with resizing last column too much (Mac OS 10.7, PySide 1.1)
        self.__ui.tableWidget.resize(self.__ui.tableWidget.width() - 1, self.__ui.tableWidget.height())
        self.__ui.tableWidget.resize(self.__ui.tableWidget.width() + 1, self.__ui.tableWidget.height())

    def addRowForExpense(self, tw, ex):
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        color = Qt.black
        if not ex.manual:
            color = Qt.gray
        tw.setItem(row, 0, self.coloredTableWidgetItem(str(ex.date.date()), color, ex))
        tw.setItem(row, 1, self.coloredTableWidgetItem(str(ex.value), color, ex))
        tw.setItem(row, 2, self.coloredTableWidgetItem(self.__envMgr.envNameForId(ex.fromId), color, ex))
        tw.setItem(row, 3, self.coloredTableWidgetItem(self.__envMgr.envNameForId(ex.toId), color, ex))
        tw.setItem(row, 4, self.coloredTableWidgetItem(ex.desc, color, ex))

    def coloredTableWidgetItem(self, text, color, userData=None):
        item = QTableWidgetItem(text)
        item.setForeground(color)
        if userData:
            item.setData(Qt.UserRole, userData)
        return item

    def addExpense(self):
        try:
            ex = self.__expMgr.addExpense(self.__ui.leExpenseUserInput.text())
            self.addRowForExpense(self.__ui.tableWidget, ex)
            self.refreshEnvelopeValues()
            self.__ui.leExpenseUserInput.setText('')
            self.showCurrentEnvelopeValue()
            self.scrollToLastExpenseRow()
        except Exception as e:
            print(e)

    def deleteExpense(self):
        items = self.__ui.tableWidget.selectedItems()
        if len(items) > 0:
            res = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this expense?",
                                       QMessageBox.Ok, QMessageBox.Cancel)
            if res == QMessageBox.Ok:
                expenses = set(i.data(Qt.UserRole) for i in items)
                for expense in expenses:
                    self.__expMgr.deleteExpense(expense)
                self.refreshEnvelopeValues()
                self.showCurrentEnvelopeValue()
                self.loadExpenses()
                self.scrollToLastExpenseRow()

    def reloadValues(self):
        self.refreshEnvelopeValues()
        self.loadExpenses()
        self.showCurrentEnvelopeValue()
        self.scrollToLastExpenseRow()

    def scrollToLastExpenseRow(self):
        tw = self.__ui.tableWidget
        item = tw.item(tw.rowCount() - 1, 0)
        tw.scrollToItem(item)

    def addEnvelope(self):
        env_name = self.__ui.leNewEnvelope.text().strip().lower()
        if env_name in (v.name.lower() for v in self.__envMgr.envelopes.values()):
            QMessageBox.warning(self, "Warning", "Envelope with given name already exists")
            return

        try:
            env = self.__envMgr.addEnvelope(env_name, u'some envelope description here')
            self.addRowForEnvelope(env)
            self.__ui.leNewEnvelope.setText('')
        except Exception as e:
            print(e)

    def refreshEnvelopeValues(self):
        tw = self.__ui.tableWidget_2
        for row in range(tw.rowCount()):
            item = tw.item(row, 0)
            envId = int(item.data(Qt.UserRole))
            item.setText(str(self.__envMgr.envelopeValue(envId)))

    def loadEnvelopes(self):
        for env in self.__envMgr.envelopes.values():
            self.addRowForEnvelope(env)
        self.__ui.tableWidget_2.resizeColumnsToContents()

    def addRowForEnvelope(self, env):
        tw = self.__ui.tableWidget_2
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        tw.setItem(row, 0, self.itemWithId(str(self.__envMgr.envelopeValue(env.id)), env.id))
        tw.setItem(row, 1, self.itemWithId(env.name, env.id))

    def itemWithId(self, itemText, itemId):
        item = QTableWidgetItem(itemText)
        item.setData(Qt.UserRole, itemId)
        return item

    def onSelectedEnvelopeChanged(self, curItem, prevItem):
        self.fillDetailTable(int(curItem.data(Qt.UserRole)))

    def fillDetailTable(self, envId):
        tw = self.__ui.tableWidget_3
        tw.clearContents()
        tw.setRowCount(0)
        for ex in self.__expMgr.expenses:
            if (ex.fromId == envId) or (ex.toId == envId):
                self.addRowForExpense(tw, ex)
        tw.resizeColumnsToContents()
