# coding=utf-8

import re
import typing as ty

from PySide6.QtCore import (
    QModelIndex,
    QPersistentModelIndex,
    QRect,
    QRectF,
    QSize,
    Qt,
)
from PySide6.QtGui import QColor, QFontMetrics, QPainter
from PySide6.QtWidgets import (
    QAbstractItemDelegate,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTreeWidget,
)

from lib.controls.pastel_colors import PastelColors
from lib.models.expense import Expense
from lib.utils import formatValue

LINE_SPACING: ty.Final = 4
MARGIN: ty.Final = 7
LEFT_MARGIN: ty.Final = 20

ModelIndex = ty.Union[QModelIndex, QPersistentModelIndex]


class ExpensesItemDelegate(QStyledItemDelegate):
    def __init__(self, delegate: QAbstractItemDelegate):
        QStyledItemDelegate.__init__(self)
        self._delegate = delegate

    def sizeHint(
        self, option: QStyleOptionViewItem, index: ModelIndex
    ) -> QSize:
        size = self._delegate.sizeHint(option, index)
        if index.parent().isValid():
            expense: Expense = index.data(Qt.ItemDataRole.UserRole)
            # For some reason PySide6 typing is missing `fontMetrics` from
            # `QStyleOption`
            fontMetrics: QFontMetrics = ty.cast(ty.Any, option).fontMetrics
            height = (
                fontMetrics.boundingRect(expense.desc).height() * 2
                + LINE_SPACING
                + 2 * MARGIN
            )
            return QSize(size.width(), height)
        else:
            return QSize(size.width(), size.height() + 5)


class ExpenseTreeWidget(QTreeWidget):
    def __init__(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        QTreeWidget.__init__(self, *args, **kwargs)
        self.setItemDelegate(ExpensesItemDelegate(self.itemDelegate()))
        self._idToName: ty.Optional[ty.Callable[[int], str]] = None

    def setIdToName(self, idToName: ty.Callable[[int], str]) -> None:
        self._idToName = idToName

    def _drawGroupRow(
        self, option: QStyleOptionViewItem, painter: QPainter, index: ModelIndex
    ) -> None:
        painter.save()
        rect: QRect = ty.cast(ty.Any, option).rect
        painter.fillRect(rect, Qt.GlobalColor.lightGray)
        painter.setPen(Qt.GlobalColor.darkGray)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        painter.setPen(QColor(Qt.GlobalColor.lightGray).lighter(120))
        painter.drawLine(rect.topLeft(), rect.topRight())
        super(QTreeWidget, self).drawRow(painter, option, index)
        painter.setPen(Qt.GlobalColor.black)
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            rect.adjusted(0, 0, -MARGIN, 0),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
            self._getSumForDay(index),
        )
        painter.restore()

    def _drawLeafRow(
        self, option: QStyleOptionViewItem, painter: QPainter, index: ModelIndex
    ) -> None:
        # For some reason PySide6 typing is missing `rect` from `QStyleOption`
        rect: QRect = ty.cast(ty.Any, option).rect
        if self.selectionModel().isSelected(index):
            painter.fillRect(rect, Qt.GlobalColor.white)
        else:
            painter.fillRect(
                rect, QColor(Qt.GlobalColor.lightGray).lighter(120)
            )
        painter.setPen(Qt.GlobalColor.darkGray)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        painter.setPen(QColor(Qt.GlobalColor.lightGray).lighter())
        painter.drawLine(rect.topLeft(), rect.topRight())
        expense: Expense = index.data(Qt.ItemDataRole.UserRole)
        painter.setPen(Qt.GlobalColor.black)
        painter.save()
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            rect.adjusted(LEFT_MARGIN, 0, 0, -rect.height() // 2),
            Qt.AlignmentFlag.AlignVCenter,
            expense.desc,
        )
        painter.restore()
        painter.setPen(Qt.GlobalColor.darkGray)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        cleanupEmojis = lambda it: re.sub(r"[\u263a-\U0001f645]", "", it)
        if self._idToName is not None:
            fromName = self._idToName(expense.fromId)
            fromRectH = painter.fontMetrics().boundingRect(
                cleanupEmojis(fromName)
            )
            fromRectW = painter.fontMetrics().boundingRect(fromName)
            fromRect = QRect(
                fromRectW.left(),
                fromRectH.top(),
                fromRectW.width(),
                fromRectH.height(),
            )
            painter.setBrush(PastelColors.color_for_string(fromName))
            painter.setPen(Qt.GlobalColor.transparent)
            bottomRect = rect.adjusted(LEFT_MARGIN, rect.height() // 2, 0, 0)
            fromRect = fromRect.adjusted(-4, -2, 4, 2)
            fromRect = QRect(
                bottomRect.left(),
                bottomRect.top(),
                fromRect.width(),
                fromRect.height(),
            )
            painter.drawRoundedRect(fromRect, 3, 3)
            painter.setPen(Qt.GlobalColor.darkGray)
            painter.drawText(
                fromRect.adjusted(4, 2, -4, -2),
                Qt.AlignmentFlag.AlignVCenter,
                fromName,
            )

            painter.save()
            # FIXME: normal check for weekly and income envelopes
            # FIXME: move colors to constants
            if not expense.manual:
                painter.setBrush(QColor(157, 157, 157))
            elif fromName.startswith("Week_"):
                painter.setBrush(Qt.GlobalColor.transparent)
            elif fromName.lower() == "доход" or fromName.lower() == "income":
                painter.setBrush(QColor(100, 230, 100))
            else:
                painter.setBrush(QColor(120, 120, 230))
            painter.setPen(Qt.GlobalColor.transparent)
            painter.drawRect(QRectF(0, rect.top() + 4, 4, rect.height() - 10))
            painter.restore()

            bottomRect = bottomRect.adjusted(fromRect.width() + MARGIN, 0, 0, 0)
            toName = self._idToName(expense.toId)
            toRectH = painter.fontMetrics().boundingRect(cleanupEmojis(toName))
            toRectW = painter.fontMetrics().boundingRect(toName)
            toRect = QRect(
                toRectW.left(), toRectH.top(), toRectW.width(), toRectH.height()
            )
            toRect = toRect.adjusted(-4, -2, 4, 2)
            toRect = QRect(
                int(bottomRect.left()),
                int(bottomRect.top()),
                toRect.width(),
                toRect.height(),
            )
            painter.setBrush(PastelColors.color_for_string(toName))
            painter.setPen(Qt.GlobalColor.transparent)
            painter.drawRoundedRect(toRect, 3, 3)
            painter.setPen(Qt.GlobalColor.darkGray)
            painter.drawText(
                toRect.adjusted(4, 2, -4, -2),
                Qt.AlignmentFlag.AlignVCenter,
                toName,
            )
        font = painter.font()
        font.setPixelSize(24)
        font.setBold(True)
        painter.save()
        painter.setFont(font)
        painter.drawText(
            rect.adjusted(rect.width() // 2, 0, -5, 0),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
            formatValue(int(expense.value)),
        )
        painter.restore()

    def _getSumForDay(self, index: ModelIndex) -> str:
        sumForDay = 0
        idx = 0
        child = index.model().index(idx, 0, index)
        while child.isValid():
            expense = child.data(Qt.ItemDataRole.UserRole)
            if expense.manual:
                if self._idToName is not None:
                    fromName = self._idToName(expense.fromId)
                    # FIXME: there should be a better way to check for the
                    #        weekly envelope
                    if not fromName.startswith("Week_"):
                        idx += 1
                        child = index.model().index(idx, 0, index)
                        continue
                sumForDay += expense.value
            idx += 1
            child = index.model().index(idx, 0, index)
        return formatValue(int(sumForDay))

    def drawRow(
        self, painter: QPainter, option: QStyleOptionViewItem, index: ModelIndex
    ) -> None:
        painter.save()
        if not index.parent().isValid():
            self._drawGroupRow(option, painter, index)
        else:
            self._drawLeafRow(option, painter, index)
        painter.restore()
