#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui

class PlannedMissionWidget(QtWidgets.QWidget):

	def __init__(self, mission = None, task_order = None):
		super().__init__()

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.box = QtWidgets.QGroupBox()
		self.main_layout.addWidget(self.box)
		self.layout = QtWidgets.QVBoxLayout()
		self.box.setLayout(self.layout)
		self.box.setFixedHeight(100)

		if mission is not None:
			self.service_label = QtWidgets.QLabel(mission.service)
			self.layout.addWidget(self.service_label)
			self.target_label = QtWidgets.QLabel(mission.target)
			self.layout.addWidget(self.target_label)

			self.dmo_dso_label = QtWidgets.QLabel("DMO : " + mission.dmo + "   DSO : " + mission.dso)
			self.layout.addWidget(self.dmo_dso_label)

			self.date_time_label = QtWidgets.QLabel(mission.time + "  " + mission.date)
			self.layout.addWidget(self.date_time_label)

			self.description_label = QtWidgets.QLabel(mission.description)

		elif task_order is not None:
			self.service_label = QtWidgets.QLabel(task_order.service)
			self.layout.addWidget(self.service_label)

			pass
