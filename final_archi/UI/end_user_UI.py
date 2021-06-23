#!/usr/bin/python3

from .custom_widgets.out_log import OutLog
from .custom_widgets.planned_mission_widget import PlannedMissionWidget

import sys
from PySide6 import QtCore, QtWidgets, QtGui

class EndUserUI(QtWidgets.QWidget):

	def __init__(self, controler):
		super().__init__()
	
		self.controler = controler

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
		self.services_box.setFixedWidth(self.services_box.parentWidget().width() * 0.6)
		self.services_box_layout = QtWidgets.QVBoxLayout()
		self.services_box.setLayout(self.services_box_layout)

		self.planned_inspection_box = QtWidgets.QGroupBox("Planned Inspections")
		self.inspection_planning_box_layout.addWidget(self.planned_inspection_box)
		self.planned_inspection_box_layout = QtWidgets.QVBoxLayout()
		self.planned_inspection_box.setLayout(self.planned_inspection_box_layout)

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

		# widgtets used in inspection planning box
		self.inspection_services_list = QtWidgets.QListWidget()
		self.inspection_services_list.itemActivated.connect(self.on_service_selected)
		# list to store widgets common to all services: widgets in this list will be removed when a nex service is selected
		self.task_order_information_widget_list_forAll = []
		# list to store widgets used not for all services 
		self.task_order_information_widget_list_custom = []
		self.info_label = QtWidgets.QLabel("Task Order Information")
		self.task_order_information_widget_list_forAll.append(self.info_label)
		self.date_label = QtWidgets.QLabel("Date")
		self.task_order_information_widget_list_forAll.append(self.date_label)
		self.date_line_edit = QtWidgets.QLineEdit()
		self.task_order_information_widget_list_forAll.append(self.date_line_edit)
		self.time_label = QtWidgets.QLabel("Time")
		self.task_order_information_widget_list_forAll.append(self.time_label)
		self.time_line_edit = QtWidgets.QLineEdit()
		self.task_order_information_widget_list_forAll.append(self.time_line_edit)


	def on_activity_selected(self, item):
		print("Activity selected : " + item.text())
		self.populate_location_box(item.text())


	def on_location_selected(self, item):
		print("Location selected : " + item.text())
		self.populate_inspection_services_box(item.text())
		self.populate_planned_inspections_box(item.text())


	def on_service_selected(self, item):
		print("Activity seleted : " + item.text())
		# self.populate_inspection_planning_box(item.text())


	def populate_location_box(self, activity_type):
		if self.location_list.parentWidget() is None:
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


	def populate_inspection_services_box(self, location):
		if self.inspection_services_list.parentWidget() is None:
			self.services_box_layout.addWidget(self.inspection_services_list)
		else:
			self.inspection_services_list.clear()

		if self.activities_list.currentItem().text() == "Airport Inspection Services":
			self.apt_serv_taxi_insp_apron = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.apt_serv_taxi_insp_apron.setText("Taxiway Apron Inspection")
			self.apt_serv_taxi_insp_light = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.apt_serv_taxi_insp_light.setText("Taxiway Lights Inspection")
			self.apt_serv_FOD = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.apt_serv_FOD.setText("FOD Detection")
			self.apt_serv_perim_surv = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.apt_serv_perim_surv.setText("Perimeter Surveillance")
			self.apt_serv_infr_insp = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.apt_serv_infr_insp.setText("Infrastructure Inspection")
		

	def populate_planned_inspections_box(self, location):
		# remove potential planned inspection for other locations
		child = self.planned_inspection_box_layout.takeAt(0)
		while child is not None:
			child.widget().setParent(None)
			# del child
			self.planned_inspection_box_layout.update()
			child = self.planned_inspection_box_layout.takeAt(0)

		# add planned inspections from already defined lists depending on the activity
		if self.activities_list.currentItem().text() == "Airport Inspection Services":
			for planned_mission in self.planed_apt_insp_list:
				planned_mission_widget = PlannedMissionWidget(planned_mission)
				self.planned_inspection_box_layout.addWidget(planned_mission_widget)
				planned_mission_widget.show()

		return


	# def populate_inspection_planning_box(self, service):
	# 	if self.task_order_information_widget_list_forAll[0].parentWidget() is None:
	# 		for widget in self.task_order_information_widget_list_forAll:
	# 			self.planned_inspection_box_layout.addWidget(widget)

	# 	index_of_last_item_to_keep = len(self.task_order_information_widget_list_forAll)
	# 	nbr_of_items = self.
	# 	for i in range nbr_of_items:

	# 	return

