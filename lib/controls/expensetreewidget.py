# coding=utf-8

from lib.utils import formatValue
from lib.controls.pastel_colors import PastelColors

from PySide2.QtWidgets import QTreeWidget, QStyleOptionViewItem, QStyledItemDelegate, QStyle
from PySide2.QtGui import QPainter, QColor
from PySide2.QtCore import Qt, QModelIndex, QSize, QPoint, QRect
import logging
import re

LINE_SPACING = 4
MARGIN = 7
LEFT_MARGIN = 20

class ExpensesItemDelegate(QStyledItemDelegate):
    def __init__(self, delegate):
        QStyledItemDelegate.__init__(self)
        self._delegate = delegate

    def sizeHint(self, option, index):
        """
        @type option: QStyleOptionViewItem
        @type index: QModelIndex
        """
        size = self._delegate.sizeHint(option, index)
        if index.parent().isValid():
            ex = index.data(Qt.UserRole)
            height = option.fontMetrics.boundingRect(ex.desc).height() * 2 + LINE_SPACING + 2 * MARGIN
            return QSize(size.width(), height)
        else:
            return QSize(size.width(), size.height() + 5)


class ExpenseTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        QTreeWidget.__init__(self, *args, **kwargs)
        self.setItemDelegate(ExpensesItemDelegate(self.itemDelegate()))
        self._idToName = None

    def setIdToName(self, idToName):
        self._idToName = idToName

    def _drawGroupRow(self, option, painter, index):
        painter.save()
        painter.fillRect(option.rect, Qt.lightGray)
        painter.setPen(Qt.darkGray)
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.setPen(QColor(Qt.lightGray).lighter(120))
        painter.drawLine(option.rect.topLeft(), option.rect.topRight())
        super(QTreeWidget, self).drawRow(painter, option, index)
        painter.setPen(Qt.black)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(option.rect.adjusted(0, 0, -MARGIN, 0), Qt.AlignVCenter | Qt.AlignRight, self._getSumForDay(index))
        painter.restore()

    def _drawLeafRow(self, option, painter, index):
        """
        @type painter: QPainter
        @type option: QStyleOptionViewItem
        @type index: QModelIndex
        """
        rect = option.rect
        if self.selectionModel().isSelected(index):
            painter.fillRect(rect, Qt.white)
        else:
            painter.fillRect(rect, QColor(Qt.lightGray).lighter(120))
        painter.setPen(Qt.darkGray)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        painter.setPen(QColor(Qt.lightGray).lighter())
        painter.drawLine(rect.topLeft(), rect.topRight())
        ex = index.data(Qt.UserRole)
        painter.setPen(Qt.black)
        painter.save()
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect.adjusted(LEFT_MARGIN, 0, 0, -rect.height() / 2), Qt.AlignVCenter, ex.desc)
        painter.restore()
        painter.setPen(Qt.darkGray)
        painter.setRenderHint(QPainter.Antialiasing)
        cleanupEmojis = lambda it: re.sub(r'[\u263a-\U0001f645]', '', fromName)
        if self._idToName is not None:
            fromName = self._idToName(ex.fromId)
            fromRectH = painter.fontMetrics().boundingRect(cleanupEmojis(fromName))
            fromRectW = painter.fontMetrics().boundingRect(fromName)
            fromRect = QRect(
                fromRectW.left(),
                fromRectH.top(),
                fromRectW.width(),
                fromRectH.height()
            )
            painter.setBrush(PastelColors.color_for_string(fromName))
            painter.setPen(Qt.transparent)
            bottomRect = rect.adjusted(LEFT_MARGIN, rect.height() / 2, 0, 0)
            fromRect = fromRect.adjusted(-4, -2, 4, 2)
            fromRect = QRect(bottomRect.left(),
                             bottomRect.top(),
                             fromRect.width(),
                             fromRect.height())
            painter.drawRoundedRect(fromRect, 3, 3)
            painter.setPen(Qt.darkGray)
            painter.drawText(fromRect.adjusted(4, 2, -4, -2), Qt.AlignVCenter, fromName)

            painter.save()
            # FIXME: normal check for weekly and income envelopes, colors to constants
            if not ex.manual:
                painter.setBrush(QColor(157, 157, 157))
            elif fromName.startswith("Week_"):
                painter.setBrush(Qt.transparent)
            elif fromName.lower() == "доход" or fromName.lower() == "income":
                painter.setBrush(QColor(100, 230, 100))
            else:
                painter.setBrush(QColor(120, 120, 230))
            painter.setPen(Qt.transparent)
            painter.drawRect(QRect(0, rect.top() + 4, 4, rect.height() - 10))
            painter.restore()

            bottomRect = bottomRect.adjusted(fromRect.width() + MARGIN, 0, 0, 0)
            toName = self._idToName(ex.toId)
            toRectH = painter.fontMetrics().boundingRect(cleanupEmojis(toName))
            toRectW = painter.fontMetrics().boundingRect(toName)
            toRect = QRect(
                toRectW.left(),
                toRectH.top(),
                toRectW.width(),
                toRectH.height()
            )
            toRect = toRect.adjusted(-4, -2, 4, 2)
            toRect = QRect(bottomRect.left(),
                           bottomRect.top(),
                           toRect.width(),
                           toRect.height())
            painter.setBrush(PastelColors.color_for_string(toName))
            painter.setPen(Qt.transparent)
            painter.drawRoundedRect(toRect, 3, 3)
            painter.setPen(Qt.darkGray)
            painter.drawText(
                toRect.adjusted(4, 2, -4, -2),
                Qt.AlignVCenter,
                toName
            )
        font = painter.font()
        font.setPixelSize(24)
        font.setBold(True)
        painter.save()
        painter.setFont(font)
        painter.drawText(
            rect.adjusted(rect.width() / 2, 0, -5, 0),
            Qt.AlignRight | Qt.AlignVCenter,
            formatValue(ex.value)
        )
        painter.restore()

    def _getSumForDay(self, index):
        """
        @type index: QModelIndex
        """
        sumForDay = 0
        idx = 0
        child = index.child(idx, 0)
        while child.isValid():
            expense = child.data(Qt.UserRole)
            if expense.manual:
                if self._idToName is not None:
                    fromName = self._idToName(expense.fromId)
                    # FIXME: there should be a better way to check for weekly envelope
                    if not fromName.startswith("Week_"):
                        idx += 1
                        child = index.child(idx, 0)
                        continue
                sumForDay += expense.value
            idx += 1
            child = index.child(idx, 0)
        return formatValue(sumForDay)

    def drawRow(self, painter, option, index):
        """
        @type painter: QPainter
        @type option: QStyleOptionViewItem
        @type index: QModelIndex
        """
        painter.save()
        if not index.parent().isValid():
            self._drawGroupRow(option, painter, index)
        else:
            self._drawLeafRow(option, painter, index)
        painter.restore()
