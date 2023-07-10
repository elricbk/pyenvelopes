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
    def __init__(self, items: list[SuggestItem]):
        super(SuggestItemListModel, self).__init__()
        self._items = items

    def rowCount(  # noqa: N802
        self, parent: ModelIndex = QtCore.QModelIndex()
    ) -> int:
        return len(self._items)

    def data(
        self,
        index: ModelIndex,
        role: int = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> ty.Any:
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._items[index.row()].displayText
        elif role == QtCore.Qt.ItemDataRole.EditRole:
            return self._items[index.row()].suggestText
        return None


class AutoCompleteEdit(QtWidgets.QLineEdit):
    def __init__(
        self,
        completions: list[str],
        separator: str = " ",
        add_space_after_completing: bool = True,
    ):
        super(AutoCompleteEdit, self).__init__()
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_InputMethodEnabled, False
        )
        self._separator = separator
        self._add_space_after_completing = add_space_after_completing
        self._completer = QtWidgets.QCompleter(completions)
        self._completer.setWidget(self)
        self._completer.setCaseSensitivity(
            QtCore.Qt.CaseSensitivity.CaseInsensitive
        )
        self._completer.popup().setAttribute(
            QtCore.Qt.WidgetAttribute.WA_InputMethodEnabled, False
        )
        self._completer.activated.connect(self._insert_completion)
        self._keys_to_ignore = [
            QtCore.Qt.Key.Key_Enter,
            QtCore.Qt.Key.Key_Return,
            QtCore.Qt.Key.Key_Escape,
            QtCore.Qt.Key.Key_Tab,
        ]

    def set_suggestions(self, items: list[SuggestItem]) -> None:
        self._completer.setModel(SuggestItemListModel(items))

    def _insert_completion(self, completion: str) -> None:
        """
        This is the event handler for the QCompleter.activated(QString) signal,
        it is called when the user selects an item in the completer popup.
        """
        extra = len(completion) - len(self._completer.completionPrefix())
        extra_text = completion[-extra:]
        if self._add_space_after_completing:
            extra_text += " "
        self.setText(self.text() + extra_text)

    def _text_under_cursor(self) -> str:
        text = self.text()
        start = text.rfind(self._separator, 0, self.cursorPosition()) + 1
        return text[start : self.cursorPosition()]

    def _update_completer_popup_items(self, prefix: str) -> None:
        """
        Filters the completer's popup items to only show items
        with the given prefix.
        """
        self._completer.setCompletionPrefix(prefix)
        self._completer.popup().setCurrentIndex(
            self._completer.completionModel().index(0, 0)
        )

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:  # noqa: N802
        if self._completer.popup().isVisible():
            if event.key() in self._keys_to_ignore:
                event.ignore()
                return
        super(AutoCompleteEdit, self).keyPressEvent(event)
        prefix = self._text_under_cursor()
        if prefix != self._completer.completionPrefix():
            self._update_completer_popup_items(prefix)
        if len(event.text()) > 0 and len(prefix) > 0:
            self._completer.complete()
        if len(prefix) == 0:
            self._completer.popup().hide()


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
