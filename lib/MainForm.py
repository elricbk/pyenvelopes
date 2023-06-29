import collections
import logging
import typing as ty
from datetime import date as Date
from datetime import datetime as DateTime

from PySide6.QtCore import Qt, QTimerEvent, Slot
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidgetItem,
)

from .BusinessPlan import BusinessPlan
from .BusinessPlanItem import BusinessPlanItem, Frequency, ItemType
from .controls.autocompleteedit import SuggestItem
from .Envelope import Envelope
from .EnvelopeManager import EnvelopeManager
from .expense import Expense
from .ExpenseManager import ExpenseManager
from .ExpenseRule import ExpenseRule
from .ExpenseRuleManager import ExpenseRuleManager
from .parse_expense import parse_expense
from .RulesAppliedManager import RulesAppliedManager
from .ui_MainForm import Ui_MainWindow
from .utils import formatValue
from .well_known_envelope import WellKnownEnvelope

# FIXME: this should be configured somehow
DAYS_TO_SHOW_THRESHOLD = 28
# FIXME: this is hardcoded Leftover envelope ID, this should be done in some
#        other way
LeftoverEnvelopeId = 3


def resizeColumnsToContents(tw: QTableWidget) -> None:
    # Workaround for https://bugreports.qt.io/browse/QTBUG-9352
    tw.setVisible(False)
    tw.resizeColumnsToContents()
    tw.horizontalHeader().setStretchLastSection(True)
    tw.setVisible(True)


class MainForm(QMainWindow):
    def __init__(self, obj: ty.Any = None) -> None:
        super(MainForm, self).__init__(obj)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self._setup_expense_table()
        self._setup_envelope_table()
        self._setup_rules_table()
        self._setup_plan_table()
        self._setup_managers()
        self._load_expenses()
        self._load_envelopes()
        self._load_rules()
        self._load_business_plan()
        self._show_this_week_envelope()
        self.__ui.twExpenses.setIdToName(self.__envMgr.envNameForId)
        self._setup_auto_completion()
        # FIXME: config or constant
        self._apply_rules_automatically()
        self.startTimer(60 * 60 * 1000)
        self.raise_()

    def _setup_auto_completion(self) -> None:
        envelopeList = [self.__envMgr.currentEnvelope]
        for envelope in self.__envMgr.envelopes.values():
            # FIXME: hack to remove weekly envelopes from autocompletion
            if envelope.name.startswith("Week_"):
                continue
            envelopeList.append(envelope)
        self.__ui.leExpenseUserInput.setModel(
            [self._envelope_to_suggest_item(e) for e in envelopeList]
        )

    def _envelope_to_suggest_item(self, env: Envelope) -> SuggestItem:
        return SuggestItem(
            displayText="%{0} [{1} руб.]".format(
                env.name, int(self.__envMgr.envelopeValue(env.id))
            ),
            suggestText="%" + env.name,
        )

    def _show_this_week_envelope(self) -> None:
        FORMAT_MESSAGE = "Current envelope ({0}): {1}"
        env = self.__envMgr.currentEnvelope
        value = formatValue(int(self.__envMgr.envelopeValue(env.id)))
        self.__ui.statusbar.showMessage(FORMAT_MESSAGE.format(env.name, value))

    def _apply_rules_automatically(self) -> None:
        if not self._need_to_apply_rules():
            return
        # FIXME: there should be transaction here -- all stuff should be done
        #        together or not at all
        self._create_envelope_for_new_week()
        self._transfer_all_from_last_week()
        self.__ruleMgr.executeAllRules()
        try:
            self._mark_week_as_rules_applied()
        except Exception:
            QMessageBox.critical(
                self,
                "Error marking this week as rules applied",
                "This error should be fixed manually",
            )
            QApplication.quit()
        self._load_expenses()

    @Slot()
    def timerEvent(self, event: QTimerEvent) -> None:
        logging.debug("Timer event for timer: %d", event.timerId())
        self._apply_rules_automatically()

    def _mark_week_as_rules_applied(self) -> None:
        self.__rulesAppliedMgr.markWeekAsRulesApplied(
            self.__envMgr.currentEnvelope.name
        )

    def _transfer_all_from_last_week(self) -> None:
        lwe = self.__envMgr.lastWeekEnvelope
        logging.debug(
            "Transferring all money (%d) from last week (%s)",
            self.__envMgr.envelopeValue(lwe.id),
            lwe.name,
        )
        self.__expMgr.addExpenseForRule(
            self.__envMgr.envelopeValue(lwe.id),
            lwe.id,
            self.__envMgr.currentEnvelope.id,
            "Transfer from previous week",
        )

    def _need_to_apply_rules(self) -> bool:
        curEnvName = self.__envMgr.currentEnvelope.name
        logging.debug(
            "Checking if need to apply rules for envelope %s", curEnvName
        )
        shouldApply = not self.__rulesAppliedMgr.rulesAppliedForWeek(curEnvName)
        logging.debug("Rules should be applied: %s", shouldApply)
        return shouldApply

    def _create_envelope_for_new_week(self) -> None:
        logging.debug("Creating envelope for current week")
        self.__expMgr.addExpenseForRule(
            self.__bp.weeklyEnvelope,
            LeftoverEnvelopeId,
            self.__envMgr.currentEnvelope.id,
            "Automatic creation of weekly envelope",
        )

    def _setup_managers(self) -> None:
        self.__expMgr = ExpenseManager()
        self.__envMgr = EnvelopeManager()
        self.__ruleMgr = ExpenseRuleManager()
        self.__bp = BusinessPlan()
        self.__rulesAppliedMgr = RulesAppliedManager()

        self.__envMgr.setExpenseManager(self.__expMgr)
        self.__ruleMgr.setExpenseManager(self.__expMgr)

    def _setup_expense_table(self) -> None:
        self.__ui.tableWidget_3.setHorizontalHeaderLabels(
            ["Дата", "Сумма", "Из", "В", "Описание"]
        )

    def _setup_envelope_table(self) -> None:
        self.__ui.tableWidget_2.setHorizontalHeaderLabels(["Сумма", "Название"])

    def _setup_rules_table(self) -> None:
        self.__ui.twRules.setHorizontalHeaderLabels(["Сумма", "Из", "В"])

    def _setup_plan_table(self) -> None:
        self.__ui.twBusinessPlan.setHorizontalHeaderLabels(
            ["Type", "Amount", "Name", "Description", "Weekly", "Envelope"]
        )
        for i in range(ItemType.ItemsCount):
            self.__ui.cbItemType.addItem(ItemType.desc(i), i)
        self.__ui.cbItemType.setCurrentIndex(1)
        for i in range(Frequency.ItemsCount):
            self.__ui.cbItemFrequency.addItem(Frequency.desc(i), i)
        self.__ui.cbItemFrequency.setCurrentIndex(4)

    @Slot()
    def addBusinessPlanItem(self) -> None:
        try:
            cbType = self.__ui.cbItemType
            cbFreq = self.__ui.cbItemFrequency
            parts = self.__ui.leNewBPItem.text().split(" ", 2)
            item = self.__bp.addItem(
                cbType.itemData(cbType.currentIndex()),
                int(parts[0]),
                parts[1],
                cbFreq.itemData(cbFreq.currentIndex()),
            )
            if item is None:
                return
            self._add_row_for_plan_item(item)
            self.__ui.leNewBPItem.setText("")
            self._show_weekly_stats()
        except Exception as e:
            print(e)

    @Slot()
    def applyBusinessPlan(self) -> None:
        self.__bp.save()
        self.__ruleMgr.clearAllRules()
        for finItem in [
            i for i in self.__bp.items if i.type == ItemType.Expense
        ]:
            try:
                envId = self.__envMgr.idForEnvName(finItem.name)
            except Exception as e:
                print(e)
                envId = self.__envMgr.addEnvelope(finItem.name).id
            self.__ruleMgr.addRule(finItem.weeklyValue, 3, envId)
        self._load_rules()
        bp = self.__bp
        QMessageBox.information(
            self,
            "Financial plan saved",
            "Weekly income: {0}\nWeekly expense: {1}\nWeekly envelope: {2}".format(
                bp.weeklyIncome, bp.weeklyExpense, bp.weeklyEnvelope
            ),
        )

    def _clear_table(self, tw: QTableWidget) -> None:
        tw.clearContents()
        tw.setRowCount(0)

    def _load_business_plan(self) -> None:
        tw = self.__ui.twBusinessPlan
        self._clear_table(tw)
        for item in self.__bp.items:
            self._add_row_for_plan_item(item)
        resizeColumnsToContents(tw)
        self._show_weekly_stats()

    def _show_weekly_stats(self) -> None:
        FORMAT_STRING = (
            "Weekly stats: Income = {0}, Expense = {1}, Envelope = {2}"
        )
        self.__ui.lblWeeklyStats.setText(
            FORMAT_STRING.format(
                formatValue(int(self.__bp.weeklyIncome)),
                formatValue(int(self.__bp.weeklyExpense)),
                formatValue(int(self.__bp.weeklyEnvelope)),
            )
        )

    def _add_row_for_plan_item(self, item: BusinessPlanItem) -> None:
        tw = self.__ui.twBusinessPlan
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        amount = formatValue(int(item.amount))
        weeklyValue = formatValue(int(item.weeklyValue))
        tw.setItem(
            row, 0, self._item_with_id(ItemType.desc(item.type), item.id)
        )
        tw.setItem(row, 1, self._item_with_id(amount, item.id))
        tw.setItem(row, 2, self._item_with_id(item.name, item.id))
        tw.setItem(
            row, 3, self._item_with_id(Frequency.desc(item.freq), item.id)
        )
        tw.setItem(row, 4, self._item_with_id(weeklyValue, item.id))
        for env in self.__envMgr.envelopes.values():
            if env.name == item.name:
                tw.setItem(row, 5, self._item_with_id("Existing", item.id))
                return
        else:
            tw.setItem(row, 5, self._item_with_id("New", item.id))

    def _load_rules(self) -> None:
        tw = self.__ui.twRules
        self._clear_table(tw)
        for rule in self.__ruleMgr.rules:
            self._add_row_for_rule(rule)
        resizeColumnsToContents(tw)

    def _add_row_for_rule(self, rule: ExpenseRule) -> None:
        tw = self.__ui.twRules
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        tw.setItem(row, 0, self._item_with_id(str(rule.amount), rule.id))
        tw.setItem(
            row,
            1,
            self._item_with_id(
                self.__envMgr.envNameForId(rule.fromId), rule.id
            ),
        )
        tw.setItem(
            row,
            2,
            self._item_with_id(self.__envMgr.envNameForId(rule.toId), rule.id),
        )

    @Slot()
    def applyRules(self) -> None:
        self.__ruleMgr.executeAllRules()
        self._load_expenses()

    def _load_expenses(self) -> None:
        self.__ui.twExpenses.clear()
        now = DateTime.now()
        dates: dict[Date, list[Expense]] = collections.defaultdict(list)
        for expense in (
            e
            for e in self.__expMgr.expenses
            if (now - e.date).days < DAYS_TO_SHOW_THRESHOLD
        ):
            dates[expense.date.date()].append(expense)
        keys = sorted(dates.keys())
        for date in keys:
            topLevelItem = self._get_top_level_item_for_date(date)
            for expense in dates[date]:
                self._add_item_for_expense(topLevelItem, expense)
        self._expand_today_top_level_item()

    def _expand_today_top_level_item(self) -> None:
        # Assure that item for today is here and expand it
        topLevelItem = self._get_top_level_item_for_date(Date.today())
        self.__ui.twExpenses.expandItem(topLevelItem)

    def _add_item_for_expense(
        self, topLevelItem: QTreeWidgetItem, expense: Expense
    ) -> None:
        expense_str = "%-5d %s\n(%s -> %s)" % (
            expense.value,
            expense.desc,
            self.__envMgr.envNameForId(expense.fromId),
            self.__envMgr.envNameForId(expense.toId),
        )
        item = QTreeWidgetItem([expense_str])
        item.setText(0, expense_str)
        item.setData(0, Qt.ItemDataRole.UserRole, expense)
        topLevelItem.insertChild(0, item)

    def _add_row_for_expense(self, tw: QTableWidget, ex: Expense) -> None:
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        color = Qt.GlobalColor.black if ex.manual else Qt.GlobalColor.gray
        value = formatValue(int(ex.value))
        tw.setItem(
            row,
            0,
            self._colored_table_widget_item(str(ex.date.date()), color, ex),
        )
        tw.setItem(row, 1, self._colored_table_widget_item(value, color, ex))
        tw.setItem(
            row,
            2,
            self._colored_table_widget_item(
                self.__envMgr.envNameForId(ex.fromId), color, ex
            ),
        )
        tw.setItem(
            row,
            3,
            self._colored_table_widget_item(
                self.__envMgr.envNameForId(ex.toId), color, ex
            ),
        )
        tw.setItem(row, 4, self._colored_table_widget_item(ex.desc, color, ex))

    def _colored_table_widget_item(
        self, text: str, color: Qt.GlobalColor, userData: ty.Any = None
    ) -> QTableWidgetItem:
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        item.setForeground(color)
        if userData:
            item.setData(Qt.ItemDataRole.UserRole, userData)
        return item

    def _get_top_level_item_for_date(self, date: Date) -> QTreeWidgetItem:
        treeWidget = self.__ui.twExpenses
        for i in range(treeWidget.topLevelItemCount()):
            item = treeWidget.topLevelItem(i)
            item_date = item.data(0, Qt.ItemDataRole.UserRole)
            if date == item_date:
                return item
        item = QTreeWidgetItem([str(date)])
        item.setData(0, Qt.ItemDataRole.UserRole, date)
        item.setText(0, (date.strftime("%A, %-d %B")))
        # FIXME: do we always need to insert at zero idx?
        treeWidget.insertTopLevelItem(0, item)
        return item

    def _expense_from_user_input(self, user_input: str) -> Expense:
        parsed_expense = parse_expense(user_input)
        envMgr = self.__envMgr
        if parsed_expense.from_envelope is WellKnownEnvelope.ThisWeek:
            parsed_expense.from_envelope = envMgr.currentEnvelope.name

        def get_envelope_id(envelope: WellKnownEnvelope | str) -> int:
            if isinstance(envelope, WellKnownEnvelope):
                return envelope.value
            else:
                return envMgr.idForEnvName(envelope)

        return Expense(
            float(parsed_expense.amount),
            parsed_expense.comment,
            get_envelope_id(parsed_expense.from_envelope),
            get_envelope_id(parsed_expense.to_envelope),
            user_input,
            True,
        )

    @Slot()
    def addExpense(self) -> None:
        user_input = self.__ui.leExpenseUserInput.text()
        expense = self._expense_from_user_input(user_input)
        self.__expMgr.add_expense(expense)
        exp_date = expense.date.date()
        topLevelItem = self._get_top_level_item_for_date(exp_date)
        self._add_item_for_expense(topLevelItem, expense)
        self._refresh_envelope_values()
        self.__ui.leExpenseUserInput.setText("")
        self._show_this_week_envelope()
        self._expand_today_top_level_item()

    @Slot()
    def deleteExpense(self) -> None:
        treeWidget = self.__ui.twExpenses
        items = [
            i
            for i in treeWidget.selectedItems()
            if treeWidget.indexOfTopLevelItem(i) == -1
        ]
        if len(items) == 0:
            return

        res = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to delete this expense?",
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Cancel,
        )
        if res == QMessageBox.StandardButton.Ok:
            expenses = set(i.data(0, Qt.ItemDataRole.UserRole) for i in items)
            for expense in expenses:
                self.__expMgr.deleteExpense(expense)
            self._refresh_envelope_values()
            self._show_this_week_envelope()
            # FIXME: fix parent's text
            for item in items:
                parent = item.parent()
                idx = parent.indexOfChild(item)
                parent.takeChild(idx)
                if parent.childCount() == 0:
                    topLevelIdx = treeWidget.indexOfTopLevelItem(parent)
                    treeWidget.takeTopLevelItem(topLevelIdx)

    @Slot()
    def reloadValues(self) -> None:
        self._refresh_envelope_values()
        self._load_expenses()
        self._show_this_week_envelope()

    @Slot()
    def addEnvelope(self) -> None:
        env_name = self.__ui.leNewEnvelope.text().strip().lower()
        if env_name in (
            v.name.lower() for v in self.__envMgr.envelopes.values()
        ):
            QMessageBox.warning(
                self, "Warning", "Envelope with given name already exists"
            )
            return

        try:
            env = self.__envMgr.addEnvelope(
                env_name, "some envelope description here"
            )
            self._add_row_for_envelope(env)
            self.__ui.leNewEnvelope.setText("")
            self._setup_auto_completion()
        except Exception:
            logging.exception("Error while adding envelope")

    def _refresh_envelope_values(self) -> None:
        tw = self.__ui.tableWidget_2
        for row in range(tw.rowCount()):
            item = tw.item(row, 0)
            envId = int(item.data(Qt.ItemDataRole.UserRole))
            item.setText(formatValue(int(self.__envMgr.envelopeValue(envId))))
        self._setup_auto_completion()

    def _load_envelopes(self) -> None:
        for env in self.__envMgr.envelopes.values():
            self._add_row_for_envelope(env)
        resizeColumnsToContents(self.__ui.tableWidget_2)

    def _add_row_for_envelope(self, env: Envelope) -> None:
        tw = self.__ui.tableWidget_2
        row = tw.rowCount()
        tw.setRowCount(row + 1)
        value = formatValue(int(self.__envMgr.envelopeValue(env.id)))
        tw.setItem(row, 0, self._item_with_id(value, env.id))
        tw.setItem(row, 1, self._item_with_id(env.name, env.id))

    def _item_with_id(self, itemText: str, itemId: ty.Any) -> QTableWidgetItem:
        item = QTableWidgetItem(itemText)
        item.setData(Qt.ItemDataRole.UserRole, itemId)
        return item

    @Slot()
    def onSelectedEnvelopeChanged(
        self, curItem: QTableWidgetItem, prevItem: QTableWidgetItem
    ) -> None:
        self.fill_detail_table(int(curItem.data(Qt.ItemDataRole.UserRole)))

    def fill_detail_table(self, envId: int) -> None:
        tw = self.__ui.tableWidget_3
        tw.setSortingEnabled(False)
        tw.clearContents()
        tw.setRowCount(0)
        for ex in self.__expMgr.expenses:
            if (ex.fromId == envId) or (ex.toId == envId):
                self._add_row_for_expense(tw, ex)
        tw.setSortingEnabled(True)
        tw.sortByColumn(0, Qt.SortOrder.DescendingOrder)
        resizeColumnsToContents(tw)
