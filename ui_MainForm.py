# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainForm.ui'
#
# Created: Sat Jul  6 00:30:37 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(549, 761)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(-1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pbDeleteExpense = QtGui.QPushButton(self.tab)
        self.pbDeleteExpense.setObjectName("pbDeleteExpense")
        self.horizontalLayout_8.addWidget(self.pbDeleteExpense)
        self.pbReload = QtGui.QPushButton(self.tab)
        self.pbReload.setObjectName("pbReload")
        self.horizontalLayout_8.addWidget(self.pbReload)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.twExpenses = ExpenseTreeWidget(self.tab)
        self.twExpenses.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.twExpenses.setAlternatingRowColors(False)
        self.twExpenses.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.twExpenses.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.twExpenses.setObjectName("twExpenses")
        self.twExpenses.headerItem().setText(0, "1")
        self.twExpenses.header().setVisible(False)
        self.verticalLayout_2.addWidget(self.twExpenses)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leExpenseUserInput = AutoCompleteEdit(self.tab)
        self.leExpenseUserInput.setObjectName("leExpenseUserInput")
        self.horizontalLayout.addWidget(self.leExpenseUserInput)
        self.btnAddExpense = QtGui.QPushButton(self.tab)
        self.btnAddExpense.setObjectName("btnAddExpense")
        self.horizontalLayout.addWidget(self.btnAddExpense)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.leNewEnvelope = QtGui.QLineEdit(self.tab_2)
        self.leNewEnvelope.setObjectName("leNewEnvelope")
        self.horizontalLayout_2.addWidget(self.leNewEnvelope)
        self.btnAddEnvelope = QtGui.QPushButton(self.tab_2)
        self.btnAddEnvelope.setObjectName("btnAddEnvelope")
        self.horizontalLayout_2.addWidget(self.btnAddEnvelope)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tableWidget_2 = QtGui.QTableWidget(self.tab_2)
        self.tableWidget_2.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(19)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.tableWidget_3 = QtGui.QTableWidget(self.tab_2)
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_3.verticalHeader().setVisible(False)
        self.tableWidget_3.verticalHeader().setDefaultSectionSize(19)
        self.verticalLayout_3.addWidget(self.tableWidget_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblRules = QtGui.QLabel(self.tab_3)
        self.lblRules.setObjectName("lblRules")
        self.verticalLayout_4.addWidget(self.lblRules)
        self.twRules = QtGui.QTableWidget(self.tab_3)
        self.twRules.setColumnCount(3)
        self.twRules.setObjectName("twRules")
        self.twRules.setColumnCount(3)
        self.twRules.setRowCount(0)
        self.twRules.horizontalHeader().setStretchLastSection(False)
        self.twRules.verticalHeader().setVisible(False)
        self.twRules.verticalHeader().setDefaultSectionSize(19)
        self.verticalLayout_4.addWidget(self.twRules)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btnApplyRules = QtGui.QPushButton(self.tab_3)
        self.btnApplyRules.setObjectName("btnApplyRules")
        self.horizontalLayout_3.addWidget(self.btnApplyRules)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblBusinessPlan = QtGui.QLabel(self.tab_4)
        self.lblBusinessPlan.setObjectName("lblBusinessPlan")
        self.verticalLayout_5.addWidget(self.lblBusinessPlan)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lblWeeklyStats = QtGui.QLabel(self.tab_4)
        self.lblWeeklyStats.setObjectName("lblWeeklyStats")
        self.horizontalLayout_7.addWidget(self.lblWeeklyStats)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.twBusinessPlan = QtGui.QTableWidget(self.tab_4)
        self.twBusinessPlan.setColumnCount(6)
        self.twBusinessPlan.setObjectName("twBusinessPlan")
        self.twBusinessPlan.setColumnCount(6)
        self.twBusinessPlan.setRowCount(0)
        self.twBusinessPlan.horizontalHeader().setStretchLastSection(True)
        self.twBusinessPlan.verticalHeader().setVisible(False)
        self.twBusinessPlan.verticalHeader().setDefaultSectionSize(19)
        self.verticalLayout_5.addWidget(self.twBusinessPlan)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbItemType = QtGui.QComboBox(self.tab_4)
        self.cbItemType.setObjectName("cbItemType")
        self.horizontalLayout_4.addWidget(self.cbItemType)
        self.leNewBPItem = QtGui.QLineEdit(self.tab_4)
        self.leNewBPItem.setObjectName("leNewBPItem")
        self.horizontalLayout_4.addWidget(self.leNewBPItem)
        self.cbItemFrequency = QtGui.QComboBox(self.tab_4)
        self.cbItemFrequency.setObjectName("cbItemFrequency")
        self.horizontalLayout_4.addWidget(self.cbItemFrequency)
        self.pbAddBPItem = QtGui.QPushButton(self.tab_4)
        self.pbAddBPItem.setObjectName("pbAddBPItem")
        self.horizontalLayout_4.addWidget(self.pbAddBPItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.pbApplyPlan = QtGui.QPushButton(self.tab_4)
        self.pbApplyPlan.setObjectName("pbApplyPlan")
        self.horizontalLayout_5.addWidget(self.pbApplyPlan)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout_6.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnAddExpense, QtCore.SIGNAL("clicked()"), MainWindow.addExpense)
        QtCore.QObject.connect(self.tableWidget_2, QtCore.SIGNAL("currentItemChanged(QTableWidgetItem*,QTableWidgetItem*)"), MainWindow.onSelectedEnvelopeChanged)
        QtCore.QObject.connect(self.leExpenseUserInput, QtCore.SIGNAL("returnPressed()"), MainWindow.addExpense)
        QtCore.QObject.connect(self.btnAddEnvelope, QtCore.SIGNAL("clicked()"), MainWindow.addEnvelope)
        QtCore.QObject.connect(self.leNewEnvelope, QtCore.SIGNAL("returnPressed()"), MainWindow.addEnvelope)
        QtCore.QObject.connect(self.btnApplyRules, QtCore.SIGNAL("clicked()"), MainWindow.applyRules)
        QtCore.QObject.connect(self.pbAddBPItem, QtCore.SIGNAL("clicked()"), MainWindow.addBusinessPlanItem)
        QtCore.QObject.connect(self.leNewBPItem, QtCore.SIGNAL("returnPressed()"), MainWindow.addBusinessPlanItem)
        QtCore.QObject.connect(self.pbApplyPlan, QtCore.SIGNAL("clicked()"), MainWindow.applyBusinessPlan)
        QtCore.QObject.connect(self.pbDeleteExpense, QtCore.SIGNAL("clicked()"), MainWindow.deleteExpense)
        QtCore.QObject.connect(self.pbReload, QtCore.SIGNAL("clicked()"), MainWindow.reloadValues)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Envelopes", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Expenses", None, QtGui.QApplication.UnicodeUTF8))
        self.pbDeleteExpense.setText(QtGui.QApplication.translate("MainWindow", "Delete Expense", None, QtGui.QApplication.UnicodeUTF8))
        self.pbReload.setText(QtGui.QApplication.translate("MainWindow", "Reload", None, QtGui.QApplication.UnicodeUTF8))
        self.leExpenseUserInput.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Enter new expense here", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddExpense.setText(QtGui.QApplication.translate("MainWindow", "Add expense", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Expenses", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Envelopes", None, QtGui.QApplication.UnicodeUTF8))
        self.leNewEnvelope.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Enter name for new envelope here", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAddEnvelope.setText(QtGui.QApplication.translate("MainWindow", "New envelope", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Expenses for selected envelope:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Envelopes", None, QtGui.QApplication.UnicodeUTF8))
        self.lblRules.setText(QtGui.QApplication.translate("MainWindow", "Rules:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApplyRules.setText(QtGui.QApplication.translate("MainWindow", "Apply rules", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Rules", None, QtGui.QApplication.UnicodeUTF8))
        self.lblBusinessPlan.setText(QtGui.QApplication.translate("MainWindow", "Business plan:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblWeeklyStats.setText(QtGui.QApplication.translate("MainWindow", "Weekly stats:", None, QtGui.QApplication.UnicodeUTF8))
        self.pbAddBPItem.setText(QtGui.QApplication.translate("MainWindow", "Add item", None, QtGui.QApplication.UnicodeUTF8))
        self.pbApplyPlan.setText(QtGui.QApplication.translate("MainWindow", "Apply plan", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Financial Plan", None, QtGui.QApplication.UnicodeUTF8))

from controls.autocompleteedit import AutoCompleteEdit
from controls.expensetreewidget import ExpenseTreeWidget
