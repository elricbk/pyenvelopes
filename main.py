from MainForm import MainForm
from PySide.QtGui import QApplication
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

app = QApplication(sys.argv)
w = MainForm()
w.show()

app.exec_()
