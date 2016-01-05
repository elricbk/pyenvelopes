from MainForm import MainForm
from PySide.QtGui import QApplication
import sys
import logging

FORMAT = "%(asctime)s - %(levelname)-8s - %(message)s"
logging.basicConfig(level=logging.DEBUG, filename='/tmp/envelopes.log', format=FORMAT)

app = QApplication(sys.argv)
w = MainForm()
w.show()

app.exec_()
