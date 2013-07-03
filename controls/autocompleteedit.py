#!/usr/bin/env python
"""
QLineEdit with autocompletion for given list of words

Found here: http://blog.elentok.com/2011/08/autocomplete-textbox-for-multiple.html
"""

from PySide import QtCore, QtGui


class AutoCompleteEdit(QtGui.QLineEdit):
    def __init__(self, model, separator=' ', addSpaceAfterCompleting=True):
        super(AutoCompleteEdit, self).__init__()
        self._separator = separator
        self._addSpaceAfterCompleting = addSpaceAfterCompleting
        self._completer = QtGui.QCompleter(model)
        self._completer.setWidget(self)
        self.connect(
            self._completer,
            QtCore.SIGNAL('activated(QString)'),
            self._insertCompletion)
        self._keysToIgnore = [QtCore.Qt.Key_Enter,
                              QtCore.Qt.Key_Return,
                              QtCore.Qt.Key_Escape,
                              QtCore.Qt.Key_Tab]

    def setModel(self, model):
        """ Set model for completion """
        self._completer.setModel(QtGui.QStringListModel(model))

    def _insertCompletion(self, completion):
        """
        This is the event handler for the QCompleter.activated(QString) signal,
        it is called when the user selects an item in the completer popup.
        """
        extra = len(completion) - len(self._completer.completionPrefix())
        extra_text = completion[-extra:]
        if self._addSpaceAfterCompleting:
            extra_text += ' '
        self.setText(self.text() + extra_text)

    def textUnderCursor(self):
        text = self.text()
        textUnderCursor = ''
        i = self.cursorPosition() - 1
        while i >= 0 and text[i] != self._separator:
            textUnderCursor = text[i] + textUnderCursor
            i -= 1
        return textUnderCursor

    def keyPressEvent(self, event):
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


    def _updateCompleterPopupItems(self, completionPrefix):
        """
        Filters the completer's popup items to only show items
        with the given prefix.
        """
        self._completer.setCompletionPrefix(completionPrefix)
        self._completer.popup().setCurrentIndex(
            self._completer.completionModel().index(0, 0))


if __name__ == '__main__':
    def demo():
        import sys

        app = QtGui.QApplication(sys.argv)
        values = ['@call', '@bug', '+qtodotxt', '+sqlvisualizer']
        editor = AutoCompleteEdit(values)
        window = QtGui.QWidget()
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(editor)
        window.setLayout(hbox)
        window.show()

        sys.exit(app.exec_())

    demo()
