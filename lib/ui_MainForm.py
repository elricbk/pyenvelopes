# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainForm.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from lib.controls.autocompleteedit import AutoCompleteEdit
from lib.controls.expensetreewidget import ExpenseTreeWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(549, 761)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_6 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
#ifndef Q_OS_MAC
        self.verticalLayout_2.setSpacing(-1)
#endif
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pbDeleteExpense = QPushButton(self.tab)
        self.pbDeleteExpense.setObjectName(u"pbDeleteExpense")

        self.horizontalLayout_8.addWidget(self.pbDeleteExpense)

        self.pbReload = QPushButton(self.tab)
        self.pbReload.setObjectName(u"pbReload")

        self.horizontalLayout_8.addWidget(self.pbReload)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.twExpenses = ExpenseTreeWidget(self.tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.twExpenses.setHeaderItem(__qtreewidgetitem)
        self.twExpenses.setObjectName(u"twExpenses")
        self.twExpenses.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.twExpenses.setAlternatingRowColors(False)
        self.twExpenses.setSelectionMode(QAbstractItemView.SingleSelection)
        self.twExpenses.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.twExpenses.header().setVisible(False)

        self.verticalLayout_2.addWidget(self.twExpenses)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leExpenseUserInput = AutoCompleteEdit(self.tab)
        self.leExpenseUserInput.setObjectName(u"leExpenseUserInput")

        self.horizontalLayout.addWidget(self.leExpenseUserInput)

        self.btnAddExpense = QPushButton(self.tab)
        self.btnAddExpense.setObjectName(u"btnAddExpense")

        self.horizontalLayout.addWidget(self.btnAddExpense)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.leNewEnvelope = QLineEdit(self.tab_2)
        self.leNewEnvelope.setObjectName(u"leNewEnvelope")

        self.horizontalLayout_2.addWidget(self.leNewEnvelope)

        self.btnAddEnvelope = QPushButton(self.tab_2)
        self.btnAddEnvelope.setObjectName(u"btnAddEnvelope")

        self.horizontalLayout_2.addWidget(self.btnAddEnvelope)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.tableWidget_2 = QTableWidget(self.tab_2)
        if (self.tableWidget_2.columnCount() < 2):
            self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(19)

        self.verticalLayout_3.addWidget(self.tableWidget_2)

        self.label_3 = QLabel(self.tab_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.tableWidget_3 = QTableWidget(self.tab_2)
        if (self.tableWidget_3.columnCount() < 5):
            self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_3.verticalHeader().setVisible(False)
        self.tableWidget_3.verticalHeader().setDefaultSectionSize(19)

        self.verticalLayout_3.addWidget(self.tableWidget_3)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_4 = QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.twRules = QTableWidget(self.tab_3)
        if (self.twRules.columnCount() < 3):
            self.twRules.setColumnCount(3)
        self.twRules.setObjectName(u"twRules")
        self.twRules.setColumnCount(3)
        self.twRules.horizontalHeader().setStretchLastSection(False)
        self.twRules.verticalHeader().setVisible(False)
        self.twRules.verticalHeader().setDefaultSectionSize(19)

        self.verticalLayout_4.addWidget(self.twRules)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.btnApplyRules = QPushButton(self.tab_3)
        self.btnApplyRules.setObjectName(u"btnApplyRules")

        self.horizontalLayout_3.addWidget(self.btnApplyRules)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_5 = QVBoxLayout(self.tab_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lblWeeklyStats = QLabel(self.tab_4)
        self.lblWeeklyStats.setObjectName(u"lblWeeklyStats")

        self.horizontalLayout_7.addWidget(self.lblWeeklyStats)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.twBusinessPlan = QTableWidget(self.tab_4)
        if (self.twBusinessPlan.columnCount() < 6):
            self.twBusinessPlan.setColumnCount(6)
        self.twBusinessPlan.setObjectName(u"twBusinessPlan")
        self.twBusinessPlan.setColumnCount(6)
        self.twBusinessPlan.horizontalHeader().setStretchLastSection(True)
        self.twBusinessPlan.verticalHeader().setVisible(False)
        self.twBusinessPlan.verticalHeader().setDefaultSectionSize(19)

        self.verticalLayout_5.addWidget(self.twBusinessPlan)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cbItemType = QComboBox(self.tab_4)
        self.cbItemType.setObjectName(u"cbItemType")

        self.horizontalLayout_4.addWidget(self.cbItemType)

        self.leNewBPItem = QLineEdit(self.tab_4)
        self.leNewBPItem.setObjectName(u"leNewBPItem")

        self.horizontalLayout_4.addWidget(self.leNewBPItem)

        self.cbItemFrequency = QComboBox(self.tab_4)
        self.cbItemFrequency.setObjectName(u"cbItemFrequency")

        self.horizontalLayout_4.addWidget(self.cbItemFrequency)

        self.pbAddBPItem = QPushButton(self.tab_4)
        self.pbAddBPItem.setObjectName(u"pbAddBPItem")

        self.horizontalLayout_4.addWidget(self.pbAddBPItem)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.pbApplyPlan = QPushButton(self.tab_4)
        self.pbApplyPlan.setObjectName(u"pbApplyPlan")

        self.horizontalLayout_5.addWidget(self.pbApplyPlan)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.tabWidget.addTab(self.tab_4, "")

        self.horizontalLayout_6.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btnAddExpense.clicked.connect(MainWindow.addExpense)
        self.tableWidget_2.currentItemChanged.connect(MainWindow.onSelectedEnvelopeChanged)
        self.leExpenseUserInput.returnPressed.connect(MainWindow.addExpense)
        self.btnAddEnvelope.clicked.connect(MainWindow.addEnvelope)
        self.leNewEnvelope.returnPressed.connect(MainWindow.addEnvelope)
        self.btnApplyRules.clicked.connect(MainWindow.applyRules)
        self.pbAddBPItem.clicked.connect(MainWindow.addBusinessPlanItem)
        self.leNewBPItem.returnPressed.connect(MainWindow.addBusinessPlanItem)
        self.pbApplyPlan.clicked.connect(MainWindow.applyBusinessPlan)
        self.pbDeleteExpense.clicked.connect(MainWindow.deleteExpense)
        self.pbReload.clicked.connect(MainWindow.reloadValues)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Envelopes", None))
        self.pbDeleteExpense.setText(QCoreApplication.translate("MainWindow", u"Delete Expense", None))
        self.pbReload.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.leExpenseUserInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter new expense here", None))
        self.btnAddExpense.setText(QCoreApplication.translate("MainWindow", u"Add expense", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Expenses", None))
        self.leNewEnvelope.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter name for new envelope here", None))
        self.btnAddEnvelope.setText(QCoreApplication.translate("MainWindow", u"New envelope", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Expenses for selected envelope:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Envelopes", None))
        self.btnApplyRules.setText(QCoreApplication.translate("MainWindow", u"Apply rules", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Rules", None))
        self.lblWeeklyStats.setText(QCoreApplication.translate("MainWindow", u"Weekly stats:", None))
        self.pbAddBPItem.setText(QCoreApplication.translate("MainWindow", u"Add item", None))
        self.pbApplyPlan.setText(QCoreApplication.translate("MainWindow", u"Apply plan", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Financial Plan", None))
    # retranslateUi

