#!/usr/bin/python3

from .custom_widgets.out_log import OutLog

import sys
from PySide6 import QtCore, QtWidgets, QtGui

class EndUserUI(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()
	
		self.setWindowTitle("END USER UI - TASK ORDER")
		self.resize(1400, 800)

		self.vert_layout = QtWidgets.QVBoxLayout(self)

		# layout to host the boxes
		self.h_layout = QtWidgets.QHBoxLayout()

		# outlog definition
		self.out_log = QtWidgets.QTextEdit()
		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.out_log.setFont(self.font)
		self.out_log.setFixedHeight(200)
		sys.stdout = OutLog(self.out_log, sys.stdout)

		# adding h_layout and outlog to vert_layout
		self.vert_layout.addLayout(self.h_layout)
		self.vert_layout.addWidget(self.out_log)

		# box definition and adding to the h_layout
		self.activities_box = QtWidgets.QGroupBox("5D Services")
		self.activities_box.setFixedWidth(self.width() / 5)
		self.h_layout.addWidget(self.activities_box)
		self.activities_box_layout = QtWidgets.QVBoxLayout()
		self.activities_box.setLayout(self.activities_box_layout)

		self.location_box = QtWidgets.QGroupBox("Location")
		self.location_box.setFixedWidth(self.width() / 5)
		self.h_layout.addWidget(self.location_box)
		self.location_box_layout = QtWidgets.QVBoxLayout()
		self.location_box.setLayout(self.location_box_layout)

		self.inspection_planning_box = QtWidgets.QGroupBox("Service selection")
		self.h_layout.addWidget(self.inspection_planning_box)
		self.inspection_planning_box_layout = QtWidgets.QHBoxLayout()
		self.inspection_planning_box.setLayout(self.inspection_planning_box_layout)

		self.services_box = QtWidgets.QGroupBox("Services")
		self.inspection_planning_box_layout.addWidget(self.services_box)

		self.planned_inspection_box = QtWidgets.QGroupBox("Planned Inspections")
		self.inspection_planning_box_layout.addWidget(self.planned_inspection_box)

		# populate the activities_box
		self.activities_list = QtWidgets.QListWidget()
		self.apt_insp_item = QtWidgets.QListWidgetItem(self.activities_list)
		self.apt_insp_item.setText('Airport Inspection Services')
		self.nav_insp_item = QtWidgets.QListWidgetItem(self.activities_list)
		self.nav_insp_item.setText('Navaids Inspection Services')
		self.wat_insp_item = QtWidgets.QListWidgetItem(self.activities_list)
		self.wat_insp_item.setText('Waterdrome Inspection Services')
		self.activities_box_layout.addWidget(self.activities_list)
		self.activities_list.itemActivated.connect(self.on_activity_selected)

		# widgets used in location box
		self.location_list = QtWidgets.QListWidget()	
		self.location_list.itemActivated.connect(self.on_location_selected)


	def on_activity_selected(self, item):
		print("Activity selected : " + item.text())
		self.populate_location_box(item.text())


	def on_location_selected(self, item):
		print("Location selected : " + item.text())
		self.populate_inspection_planning_box(item.text())


	def populate_location_box(self, activity_type):
		if self.location_list is None:
			self.location_box_layout.addWidget(self.location_list)
		else:
			self.location_list.clear()

		if activity_type == "Airport Inspection Services":
			self.location_heathrow = QtWidgets.QListWidgetItem(self.location_list)
			self.location_heathrow.setText("Heathrow Airport")
		elif activity_type == "Navaids Inspection Services":
			self.location_rhodes = QtWidgets.QListWidgetItem(self.location_list)
			self.location_rhodes.setText("Rhodes Airport")
		elif activity_type == "Waterdrome Inspection Services":
			self.location_corfu = QtWidgets.QListWidgetItem(self.location_list)
			self.location_corfu.setText("Corfu Waterdrome")

		self.loc2 = QtWidgets.QListWidgetItem(self.location_list)
		self.loc2.setText("Location 2")
		self.loc3 = QtWidgets.QListWidgetItem(self.location_list)
		self.loc3.setText("Location 3")


	# def populate_inspection_planning_box(self, location):
		