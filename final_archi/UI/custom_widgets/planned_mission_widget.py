#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui

class PlannedMissionWidget(QtWidgets.QWidget):

	def __init__(self, args):
		super().__init__()

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.date_label = QtWidgets.QLabel(args["date"])
		self.main_layout.addWidget(self.date_label)
