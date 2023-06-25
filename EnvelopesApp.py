#!/usr/bin/env python3
import logging
import sys

from PySide6.QtWidgets import QApplication

from lib.MainForm import MainForm

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="/tmp/envelopes.log",
        format="%(asctime)s - %(levelname)-8s - %(message)s",
    )

    app = QApplication(sys.argv)
    w = MainForm()
    w.show()

    app.exec()
