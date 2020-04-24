from PyQt5.QtWidgets import QDialog
from PyQt5 import uic


class LogDialog(QDialog):
    def __init__(self, parent):
        super(LogDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi("/home/marcin/dev/studies/Heuristics-Miner/implementation/app/ui/log_dialog.ui", self)
        self.show()

    def get_state(self):
        return {
            "timestamp_column": self.timestamp_column_combobox.currentText(),
            "case_column": self.case_column_combobox.currentText(),
            "activity_column": self.activity_column_combobox.currentText()
        }

    def set_columns(self, columns):
        self.timestamp_column_combobox.addItems(columns)
        self.case_column_combobox.addItems(columns)
        self.activity_column_combobox.addItems(columns)

    @staticmethod
    def get_columns(columns, parnet=None):
        dialog = LogDialog(parnet)
        dialog.set_columns(columns)
        if dialog.exec_():
            return dialog.get_state()
