from MainForm import MainForm
from PySide.QtGui import QApplication
import sys

app = QApplication(sys.argv)
w = MainForm()
w.show()

app.exec_()
