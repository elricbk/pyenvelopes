#!/usr/bin/env python3
from lib.MainForm import MainForm
from PySide6.QtWidgets import QApplication
import sys
import logging

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/envelopes.log',
        format="%(asctime)s - %(levelname)-8s - %(message)s"
    )

    app = QApplication(sys.argv)
    w = MainForm()
    w.show()

    app.exec()
