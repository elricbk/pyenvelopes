#!/usr/bin/env python3
"""
QLineEdit with autocompletion for given list of words

Found here: http://blog.elentok.com/2011/08/autocomplete-textbox-for-multiple.html
"""

import collections
import typing as ty

from PySide6 import QtCore, QtGui, QtWidgets

SuggestItem = collections.namedtuple("SuggestItem", "displayText,suggestText")
ModelIndex = ty.Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]


class SuggestItemListModel(QtCore.QAbstractListModel):
    def __init__(self, suggestItemList: list[SuggestItem]):
        super(SuggestItemListModel, self).__init__()
        self.__suggestItemList = suggestItemList

    def rowCount(self, parent: ModelIndex = QtCore.QModelIndex()) -> int:
        return len(self.__suggestItemList)

    def data(
        self,
        modelIndex: ModelIndex,
        role: int = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> ty.Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.__suggestItemList[modelIndex.row()].displayText
        elif role == QtCore.Qt.ItemDataRole.EditRole:
            return self.__suggestItemList[modelIndex.row()].suggestText
        return None


class AutoCompleteEdit(QtWidgets.QLineEdit):
    def __init__(
        self,
        model: list[str],
        separator: str = " ",
        addSpaceAfterCompleting: bool = True,
    ):
        super(AutoCompleteEdit, self).__init__()
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_InputMethodEnabled, False
        )
        self._separator = separator
        self._addSpaceAfterCompleting = addSpaceAfterCompleting
        self._completer = QtWidgets.QCompleter(model)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive
        )
        self._completer.popup().setAttribute(
            QtCore.Qt.WidgetAttribute.WA_InputMethodEnabled, False
        )
        self._completer.activated.connect(self._insertCompletion)
        self._keysToIgnore = [
            QtCore.Qt.Key.Key_Enter,
            QtCore.Qt.Key.Key_Return,
            QtCore.Qt.Key.Key_Escape,
            QtCore.Qt.Key.Key_Tab,
        ]

    def setModel(self, suggestItemList: list[SuggestItem]) -> None:
        """Set model for completion"""
        self._completer.setModel(SuggestItemListModel(suggestItemList))

    def _insertCompletion(self, completion: str) -> None:
        """
        This is the event handler for the QCompleter.activated(QString) signal,
        it is called when the user selects an item in the completer popup.
        """
        extra = len(completion) - len(self._completer.completionPrefix())
        extra_text = completion[-extra:]
        if self._addSpaceAfterCompleting:
            extra_text += " "
        self.setText(self.text() + extra_text)

    def textUnderCursor(self) -> str:
        text = self.text()
        textUnderCursor = ""
        i = self.cursorPosition() - 1
        while i >= 0 and text[i] != self._separator:
            textUnderCursor = text[i] + textUnderCursor
            i -= 1
        return textUnderCursor

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if self._completer.popup().isVisible():
            if event.key() in self._keysToIgnore:
                event.ignore()
                return
        super(AutoCompleteEdit, self).keyPressEvent(event)
        completionPrefix = self.textUnderCursor()
        if completionPrefix != self._completer.completionPrefix():
            self._updateCompleterPopupItems(completionPrefix)
        if len(event.text()) > 0 and len(completionPrefix) > 0:
            self._completer.complete()
        if len(completionPrefix) == 0:
            self._completer.popup().hide()

    def _updateCompleterPopupItems(self, completionPrefix: str) -> None:
        """
        Filters the completer's popup items to only show items
        with the given prefix.
        """
        self._completer.setCompletionPrefix(completionPrefix)
        self._completer.popup().setCurrentIndex(
            self._completer.completionModel().index(0, 0)
        )


if __name__ == "__main__":

    def demo() -> None:
        import sys

        from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

        app = QApplication(sys.argv)
        values = ["@call", "@bug", "+qtodotxt", "+sqlvisualizer"]
        editor = AutoCompleteEdit(values)
        window = QWidget()
        hbox = QHBoxLayout()
        hbox.addWidget(editor)
        window.setLayout(hbox)
        window.show()

        sys.exit(app.exec())

    demo()
