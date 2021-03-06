# encoding: utf-8
import logging
import datetime

from PySide2.QtWidgets import QMainWindow, QApplication, QListWidget, QListWidgetItem
from PySide2.QtWidgets import QTableWidgetItem, QMessageBox, QTreeWidgetItem
from PySide2.QtCore import Qt

from .ui_MainForm import Ui_MainWindow
from .ExpenseManager import ExpenseManager
from .EnvelopeManager import EnvelopeManager, make_facade
from .ExpenseRuleManager import ExpenseRuleManager
from .BusinessPlan import BusinessPlan
from .BusinessPlanItem import Frequency, ItemType
from .RulesAppliedManager import RulesAppliedManager
from .controls.autocompleteedit import SuggestItem
from .utils import formatValue

# FIXME: this should be configured somehow
DAYS_TO_SHOW_THRESHOLD = 28
# FIXME: this is hardcoded Leftover envelope ID, this should be done not this way
LeftoverEnvelopeId = 3

def resizeColumnsToContents(tw):
    """
    @type tw: QTableWidget
    """
    # Workaround for https://bugreports.qt.io/browse/QTBUG-9352
    tw.setVisible(False)
    tw.resizeColumnsToContents()
    tw.horizontalHeader().setStretchLastSection(True)
    tw.setVisible(True)

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
        self.__ui.twExpenses.setIdToName(self.__envMgr.envNameForId)
        self.setupAutoCompletion()
        # FIXME: config or constant
        self.applyRulesAutomatically()
        self.startTimer(60 * 60 * 1000)
        self.raise_()

    def setupAutoCompletion(self):
        envelopeList = [self.__envMgr.currentEnvelope]
        for envelope in self.__envMgr.envelopes.values():
            # FIXME: this is a hack to remove weekly envelopes from autocompletion
            if envelope.name.startswith("Week_"):
                continue
            envelopeList.append(envelope)
        self.__ui.leExpenseUserInput.setModel(
            self.__envelopeToSuggestItem(e) for e in envelopeList
        )

    def __envelopeToSuggestItem(self, env):
        return SuggestItem(
            displayText="%{0} [{1} руб.]".format(
                env.name,
                int(self.__envMgr.envelopeValue(env.id))
            ),
            suggestText="%" + env.name
        )

    def showCurrentEnvelopeValue(self):
        FORMAT_MESSAGE = "Current envelope ({0}): {1}"
        env = self.__envMgr.currentEnvelope
        value = formatValue(self.__envMgr.envelopeValue(env.id))
        self.__ui.statusbar.showMessage(FORMAT_MESSAGE.format(env.name, value))

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
            "Transfer from previous week"
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

        self.__expMgr.setEnvelopeManager(make_facade(self.__envMgr))
        self.__envMgr.setExpenseManager(self.__expMgr)
        self.__ruleMgr.setExpenseManager(self.__expMgr)

    def setupExpenseTable(self):
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
        resizeColumnsToContents(tw)
        self.showWeeklyStats()

    def showWeeklyStats(self):
        FORMAT_STRING = "Weekly stats: Income = {0}, Expense = {1}, Envelope = {2}"
        self.__ui.lblWeeklyStats.setText(FORMAT_STRING.format(
            formatValue(self.__bp.weeklyIncome),
            formatValue(self.__bp.weeklyExpense),
            formatValue(self.__bp.weeklyEnvelope)
        ))

    def addRowForPlanItem(self, item):
        tw = self.__ui.twBusinessPlan
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        amount = formatValue(item.amount)
        weeklyValue = formatValue(item.weeklyValue)
        tw.setItem(row, 0, self.itemWithId(ItemType.desc(item.type), item.id))
        tw.setItem(row, 1, self.itemWithId(amount, item.id))
        tw.setItem(row, 2, self.itemWithId(item.name, item.id))
        tw.setItem(row, 3, self.itemWithId(Frequency.desc(item.freq), item.id))
        tw.setItem(row, 4, self.itemWithId(weeklyValue, item.id))
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
        resizeColumnsToContents(tw)

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
        self.__ui.twExpenses.clear()
        now = datetime.datetime.now()
        dates = {}
        for ex in (e for e in self.__expMgr.expenses if (now - e.date).days < DAYS_TO_SHOW_THRESHOLD):
            date = ex.date.date()
            if date in dates:
                dates[date].append(ex)
            else:
                dates[date] = [ex]
        keys = sorted(dates.keys())
        for date in keys:
            topLevelItem = self.getTopLevelItemForDate(self.__ui.twExpenses, date)
            for ex in dates[date]:
                self.addItemForExpense(topLevelItem, ex)
        self.expandTodayTopLevelItem()

    def expandTodayTopLevelItem(self):
        # Assure that item for today is here and expand it
        topLevelItem = self.getTopLevelItemForDate(self.__ui.twExpenses, datetime.datetime.now().date())
        self.__ui.twExpenses.expandItem(topLevelItem)
        # HACK: removes glitch with resizing last column too much (Mac OS 10.7, PySide 1.1)
        self.__ui.twExpenses.resize(self.__ui.twExpenses.width() - 1, self.__ui.twExpenses.height())
        self.__ui.twExpenses.resize(self.__ui.twExpenses.width() + 1, self.__ui.twExpenses.height())

    def addItemForExpense(self, topLevelItem, ex):
        ex_str = "%-5d %s\n(%s -> %s)" % (ex.value, ex.desc, self.__envMgr.envNameForId(ex.fromId),
            self.__envMgr.envNameForId(ex.toId))
        ex_item = QTreeWidgetItem([ex_str])
        ex_item.setText(0, ex_str)
        ex_item.setData(0, Qt.UserRole, ex)
        topLevelItem.insertChild(0, ex_item)

    def addRowForExpense(self, tw, ex):
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        color = Qt.black if ex.manual else Qt.gray
        value = formatValue(ex.value)
        tw.setItem(row, 0, self.coloredTableWidgetItem(str(ex.date.date()), color, ex))
        tw.setItem(row, 1, self.coloredTableWidgetItem(value, color, ex))
        tw.setItem(row, 2, self.coloredTableWidgetItem(self.__envMgr.envNameForId(ex.fromId), color, ex))
        tw.setItem(row, 3, self.coloredTableWidgetItem(self.__envMgr.envNameForId(ex.toId), color, ex))
        tw.setItem(row, 4, self.coloredTableWidgetItem(ex.desc, color, ex))

    def coloredTableWidgetItem(self, text, color, userData=None):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item.setForeground(color)
        if userData:
            item.setData(Qt.UserRole, userData)
        return item

    def getTopLevelItemForDate(self, tw, date):
        """
        @type tw: QListWidget
        """
        for i in range(tw.topLevelItemCount()):
            item = tw.topLevelItem(i)
            if item is None:
                continue
            item_date = item.data(0, Qt.UserRole)
            if date == item_date:
                return item
        item = QTreeWidgetItem([str(date)])
        item.setData(0, Qt.UserRole, date)
        item.setText(0, (date.strftime("%A, %-d %B")))
        # FIXME: do we always need to insert at zero idx?
        tw.insertTopLevelItem(0, item)
        return item

    def addExpense(self):
        ex = self.__expMgr.addExpense(self.__ui.leExpenseUserInput.text())
        tw = self.__ui.twExpenses
        exp_date = ex.date.date()
        topLevelItem = self.getTopLevelItemForDate(tw, exp_date)
        self.addItemForExpense(topLevelItem, ex)
        self.refreshEnvelopeValues()
        self.__ui.leExpenseUserInput.setText('')
        self.showCurrentEnvelopeValue()
        self.expandTodayTopLevelItem()

    def deleteExpense(self):
        tw = self.__ui.twExpenses
        items = [i for i in tw.selectedItems() if tw.indexOfTopLevelItem(i) == -1]
        if len(items) > 0:
            res = QMessageBox.question(self, "Confirmation", "Are you sure you want to delete this expense?",
                                       QMessageBox.Ok, QMessageBox.Cancel)
            if res == QMessageBox.Ok:
                expenses = set(i.data(0, Qt.UserRole) for i in items)
                for expense in expenses:
                    self.__expMgr.deleteExpense(expense)
                self.refreshEnvelopeValues()
                self.showCurrentEnvelopeValue()
                # FIXME: fix parent's text
                for item in items:
                    parent = item.parent()
                    idx = parent.indexOfChild(item)
                    parent.takeChild(idx)
                    if parent.childCount() == 0:
                        topLevelIdx = tw.indexOfTopLevelItem(parent)
                        tw.takeTopLevelItem(topLevelIdx)
                # self.loadExpenses()
                # self.scrollToLastExpenseRow()

    def reloadValues(self):
        self.refreshEnvelopeValues()
        self.loadExpenses()
        self.showCurrentEnvelopeValue()
        # self.scrollToLastExpenseRow()

    def scrollToLastExpenseRow(self):
        tw = self.__ui.twExpenses
        item = tw.item(tw.rowCount() - 1, 0)
        tw.scrollToItem(item)

    def addEnvelope(self):
        env_name = self.__ui.leNewEnvelope.text().strip().lower()
        if env_name in (v.name.lower() for v in self.__envMgr.envelopes.values()):
            QMessageBox.warning(self, "Warning", "Envelope with given name already exists")
            return

        try:
            env = self.__envMgr.addEnvelope(env_name, 'some envelope description here')
            self.addRowForEnvelope(env)
            self.__ui.leNewEnvelope.setText('')
            self.setupAutoCompletion()
        except Exception as e:
            logging.exception("Error while adding envelope")

    def refreshEnvelopeValues(self):
        tw = self.__ui.tableWidget_2
        for row in range(tw.rowCount()):
            item = tw.item(row, 0)
            envId = int(item.data(Qt.UserRole))
            item.setText(formatValue(self.__envMgr.envelopeValue(envId)))
        self.setupAutoCompletion()

    def loadEnvelopes(self):
        for env in self.__envMgr.envelopes.values():
            self.addRowForEnvelope(env)
        resizeColumnsToContents(self.__ui.tableWidget_2)

    def addRowForEnvelope(self, env):
        tw = self.__ui.tableWidget_2
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        value = formatValue(self.__envMgr.envelopeValue(env.id))
        tw.setItem(row, 0, self.itemWithId(value, env.id))
        tw.setItem(row, 1, self.itemWithId(env.name, env.id))

    def itemWithId(self, itemText, itemId):
        item = QTableWidgetItem(itemText)
        item.setData(Qt.UserRole, itemId)
        return item

    def onSelectedEnvelopeChanged(self, curItem, prevItem):
        self.fillDetailTable(int(curItem.data(Qt.UserRole)))

    def fillDetailTable(self, envId):
        tw = self.__ui.tableWidget_3
        tw.setSortingEnabled(False)
        tw.clearContents()
        tw.setRowCount(0)
        for ex in self.__expMgr.expenses:
            if (ex.fromId == envId) or (ex.toId == envId):
                self.addRowForExpense(tw, ex)
        tw.setSortingEnabled(True)
        tw.sortByColumn(0, Qt.DescendingOrder)
        resizeColumnsToContents(tw)
