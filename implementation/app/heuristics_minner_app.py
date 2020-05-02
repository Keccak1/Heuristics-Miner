import csv
import sys
import os

from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QApplication, QLabel, QFileDialog, QMessageBox, QDesktopWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt

from implementation.app.log_dialog import LogDialog
from implementation.heuristics_minner import HeuristicsMinner
from implementation.log_parsers.csv_parser import from_csv, DtType


class HeuristicsMinnerApp(QMainWindow):

    def __init__(self):
        super(HeuristicsMinnerApp, self).__init__()
        self._minner = None
        self.setup_ui()

    def setup_ui(self):
        uic.loadUi(
            "/home/marcin/dev/studies/Heuristics-Miner/implementation/app/ui/heuristics.ui", self)
        self._setup_sliders()
        self._setup_buttons()
        self._setup_checkboxes()
        self.center()
        self.show()

    def _setup_buttons(self):
        self.load_push_button.clicked.connect(self.load_log_dialog)
        self.draw_push_button.clicked.connect(self.draw)

    def _setup_checkboxes(self):
        self.all_task_connected_checkbox.toggled.connect(
            self._update_all_task_connected_value)
        self.long_distance_dependance_checkbox.toggled.connect(
            self._update_long_distance_dependance_value)
        self.ignore_loop_dependency_threshold_checkbox.toggled.connect(
            self._update_ignore_loop_dependency_threshold_value)

    def _update_long_distance_dependance_value(self):
        if self._minner:
            self.draw()

    def _update_ignore_loop_dependency_threshold_value(self):
        if self._minner:
            self.draw()

    def _update_all_task_connected_value(self):
        if self._minner:
            self._minner.set_all_task_connected(
                self.all_task_connected_checkbox.isChecked())

    def _setup_sliders(self):
        self.relative_to_best_slider.setRange(0, 100)
        self.length_two_loops_slider.setRange(0, 100)
        self.length_one_loops_slider.setRange(0, 100)
        self.dependency_slider.setRange(0, 100)
        self.long_distance_slider.setRange(0, 100)

        self.relative_to_best_slider.valueChanged.connect(
            self.update_relative_to_best_value)
        self.length_two_loops_slider.valueChanged.connect(
            self.update_length_two_loops_value)
        self.length_one_loops_slider.valueChanged.connect(
            self.update_length_one_loops_value)
        self.dependency_slider.valueChanged.connect(
            self.update_dependecy_value)
        self.long_distance_slider.valueChanged.connect(
            self.update_long_distance_value)

    @staticmethod
    def get_slider_value(slider):
        slider_value = str(slider.value()/100)
        return slider_value if len(slider_value) != 3 else "".join([slider_value, "0"])

    @staticmethod
    def get_columns(log_filename):
        with open(log_filename, newline='') as f:
            columns = next(csv.reader(f))
        return columns

    def center(self):
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def update_relative_to_best_value(self):
        value = HeuristicsMinnerApp.get_slider_value(
            self.relative_to_best_slider)
        self.relative_to_best_value.setText(value)

        if self._minner:
            self._minner.set_relative_to_best_threshold(float(value))

    def update_length_two_loops_value(self):
        value = HeuristicsMinnerApp.get_slider_value(
            self.length_two_loops_slider)
        self.length_two_loops_value.setText(value)

        if self._minner:
            self._minner.set_two_length_loops_threshold(float(value))

    def update_length_one_loops_value(self):
        value = HeuristicsMinnerApp.get_slider_value(
            self.length_one_loops_slider)
        self.length_one_loops_value.setText(value)

        if self._minner:
            self._minner.set_one_length_loops_threshold(float(value))

    def update_dependecy_value(self):
        value = HeuristicsMinnerApp.get_slider_value(
            self.dependency_slider)
        self.dependency_value.setText(value)

        if self._minner:
            self._minner.set_dependency_threshold(float(value))

    def update_long_distance_value(self):
        value = HeuristicsMinnerApp.get_slider_value(
            self.long_distance_slider)
        self.long_distance_value.setText(value)

        if self._minner:
            self._minner.set_long_distance_threshold(float(value))

    def load_log_dialog(self):
        log_file = QFileDialog.getOpenFileName(self,
                                               "Open log",
                                               str(os.getcwd()),
                                               "Log files (*.csv)")[0]

        if log_file:
            self.setup_columns(log_file)

    def setup_columns(self, log_file):
        log_dialog = LogDialog.get_columns(
            HeuristicsMinnerApp.get_columns(log_file), self)

        if log_dialog and len(log_dialog.values()) != len(list(set(log_dialog.values()))):
            self.print_error_msg(QMessageBox.Critical,
                                 "Not valid columns",
                                 "Name of columns should be unique for timestamp, activity and case.")

            self.status_value_label.setText("Log not loaded")

        else:
            self.status_value_label.setText("Log loaded")
            self.setup_heuristics_minner(log_file, log_dialog)

        self.status_value_label.setStyleSheet("font-size: 20px")

    def _update_parameters(self):
        if self._minner:
            relative_to_best_threshold = float(
                self.relative_to_best_value.text())
            dependency_threshold = float(self.dependency_value.text())
            length_one_loops_threshold = float(
                self.length_one_loops_value.text())
            length_two_loops_threshold = float(
                self.length_two_loops_value.text())
            long_distance_threshold = float(self.long_distance_value.text())
            all_task_connected = self.all_task_connected_checkbox.isChecked()
            ignore_loop_dependency_threshold = self.ignore_loop_dependency_threshold_checkbox.isChecked()
            ignore_long_distance_dependance_threshold = self.long_distance_dependance_checkbox.isChecked()

            long_distance_threshold = long_distance_threshold if (
                not ignore_loop_dependency_threshold and not ignore_long_distance_dependance_threshold) else 0

            self._minner.set_long_distance_threshold(long_distance_threshold)
            self._minner.set_one_length_loops_threshold(length_one_loops_threshold)
            self._minner.set_two_length_loops_threshold(length_two_loops_threshold)
            self._minner.set_direct_dependecy_matrix_params(dependency_threshold,
                                                            relative_to_best_threshold,
                                                            all_task_connected)

    def setup_heuristics_minner(self, log_file, columns):

        log = from_csv(log_file, columns["case_column"],
                       columns["activity_column"],
                       columns["timestamp_column"],
                       dt_type=DtType.TIMESTAMP)

        self._minner = HeuristicsMinner.from_log(log)
        print(self._minner.events_amount)
        self.draw()

    def draw(self):

        if self._minner:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self._update_parameters()        
            self._minner.update()
            QApplication.restoreOverrideCursor()
        else:
            self.print_error_msg(QMessageBox.Critical, "Minner not created",
                                 "Load data and create heuristics minner first.")

    def print_error_msg(self, msg_type, title, text):
        msg = QMessageBox(self)
        msg.setIcon(msg_type)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()
