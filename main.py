import sys
from PyQt5.QtWidgets import QApplication

import implementation.heuristics_minner
from implementation.app.heuristics_minner_app import HeuristicsMinnerApp

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
# this line allows kill the program by SIGINT signal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    minner_app = HeuristicsMinnerApp()
    app.exec_()
