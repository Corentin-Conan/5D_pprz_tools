#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui

class PlannedMissionWidget(QtWidgets.QWidget):

	def __init__(self, mission):
		super().__init__()

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.date_label = QtWidgets.QLabel(mission.date)
		self.main_layout.addWidget(self.date_label)

	def create_from_mission(self, mission):
		return
