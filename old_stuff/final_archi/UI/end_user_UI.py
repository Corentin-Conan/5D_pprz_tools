#!/usr/bin/python3

from .custom_widgets.out_log import OutLog
from .custom_widgets.planned_mission_widget import PlannedMissionWidget

from .DMO_DSO_UI import DMODSOUI

import sys
from PySide6 import QtCore, QtWidgets, QtGui

class EndUserUI(QtWidgets.QWidget):

	def __init__(self, mission_manager, request_manager):
		super().__init__()
	
		self.mission_manager = mission_manager

		self.request_manager = request_manager

		self.setWindowTitle("END USER UI - TASK ORDER")
		self.resize(1400, 700)

		self.vert_layout = QtWidgets.QVBoxLayout(self)

		# layout to host the boxes
		self.h_layout = QtWidgets.QHBoxLayout()

		# outlog definition
		# self.out_log = QtWidgets.QTextEdit()
		# self.font = QtGui.QFont()
		# self.font.setPointSize(8)
		# self.out_log.setFont(self.font)
		# self.out_log.setFixedHeight(200)
		# sys.stdout = OutLog(self.out_log, sys.stdout)

		# adding h_layout and outlog to vert_layout
		self.vert_layout.addLayout(self.h_layout)
		# self.vert_layout.addWidget(self.out_log)

		#vert layout for 5D services and location box
		self.left_v_layout = QtWidgets.QVBoxLayout()
		self.h_layout.addLayout(self.left_v_layout)

		# box definition and adding to the h_layout
		self.activities_box = QtWidgets.QGroupBox("5D Services")
		self.activities_box.setFixedWidth(self.width() / 5)
		self.left_v_layout.addWidget(self.activities_box)
		self.activities_box.setFixedHeight(self.activities_box.parentWidget().height() / 3)
		self.activities_box_layout = QtWidgets.QVBoxLayout()
		self.activities_box.setLayout(self.activities_box_layout)

		self.location_box = QtWidgets.QGroupBox("Location")
		self.location_box.setFixedWidth(self.width() / 5)
		self.left_v_layout.addWidget(self.location_box)
		self.location_box_layout = QtWidgets.QVBoxLayout()
		self.location_box.setLayout(self.location_box_layout)

		self.inspection_planning_box = QtWidgets.QGroupBox("Service selection")
		self.h_layout.addWidget(self.inspection_planning_box)
		self.inspection_planning_box_layout = QtWidgets.QHBoxLayout()
		self.inspection_planning_box.setLayout(self.inspection_planning_box_layout)

		self.services_box = QtWidgets.QGroupBox("Services")
		self.inspection_planning_box_layout.addWidget(self.services_box)
		self.services_box.setFixedWidth(self.services_box.parentWidget().width() * 0.5)
		self.services_box_layout = QtWidgets.QVBoxLayout()
		self.services_box.setLayout(self.services_box_layout)

		self.service_detail_box = QtWidgets.QGroupBox("Service Details")
		self.inspection_planning_box_layout.addWidget(self.service_detail_box)
		self.service_detail_box.setFixedWidth(self.service_detail_box.parentWidget().width() * 0.6)
		self.service_detail_box_layout = QtWidgets.QFormLayout()
		self.service_detail_box.setLayout(self.service_detail_box_layout)

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

		# widgets used in inspection planning box
		self.inspection_services_list = QtWidgets.QListWidget()
		self.inspection_services_list.itemActivated.connect(self.on_service_selected)
		# list to store widgets common to all services: widgets in this list will be removed when a nex service is selected
		self.task_order_information_widget_list_forAll = []
		# list to store widgets used not for all services 
		self.task_order_information_widget_list_custom = []
		self.date_label = QtWidgets.QLabel("Date")
		self.date_line_edit = QtWidgets.QLineEdit()
		self.task_order_information_widget_list_forAll.append((self.date_label, self.date_line_edit))
		self.time_label = QtWidgets.QLabel("Time")
		self.time_line_edit = QtWidgets.QLineEdit()
		self.task_order_information_widget_list_forAll.append((self.time_label, self.time_line_edit))
		self.target_label = QtWidgets.QLabel("Inspection Target")
		self.target_line_edit = QtWidgets.QLineEdit()
		self.task_order_information_widget_list_forAll.append((self.target_label, self.target_line_edit))
		self.send_task_order_button = QtWidgets.QPushButton("Send task order")
		self.send_task_order_button.clicked.connect(self.send_task_order)
		self.task_order_information_widget_list_forAll.append((self.send_task_order_button, None))


	def on_activity_selected(self, item):
		print("Activity selected : " + item.text())
		self.populate_location_box(item.text())


	def on_location_selected(self, item):
		print("Location selected : " + item.text())
		self.populate_inspection_services_box(item.text())
		self.populate_planned_inspections_box()


	def on_service_selected(self, item):
		print("Service seleted : " + item.text())
		self.populate_inspection_planning_box(item.text())


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
		elif self.activities_list.currentItem().text() == "Navaids Inspection Services":
			self.navaid_serv_vor_ext_ground_test = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.navaid_serv_vor_ext_ground_test.setText("VOR Extended Ground Test")
			self.navaid_serv_vor_short_range_flight_test = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.navaid_serv_vor_short_range_flight_test.setText("VOR Short Range Flight Test")
			self.navaid_serv_dme_dme_eval = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.navaid_serv_dme_dme_eval.setText("DME DME Evaluation")
		elif self.activities_list.currentItem().text() == "Waterdrome Inspection Services":
			self.waterdrome_serv_infr_insp = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.waterdrome_serv_infr_insp.setText("Infrastructure Inspection")
			self.waterdrome_serv_watway_insp = QtWidgets.QListWidgetItem(self.inspection_services_list)
			self.waterdrome_serv_watway_insp.setText("Waterway Inspection")


	def populate_planned_inspections_box(self):
		# remove potential planned inspection for other locations
		child = self.planned_inspection_box_layout.takeAt(0)
		while child is not None :
			if child.widget() is not None:
				child.widget().setParent(None)
			self.planned_inspection_box_layout.update()
			child = self.planned_inspection_box_layout.takeAt(0)

		# add planned inspections from already defined lists depending on the activity
		if self.activities_list.currentItem().text() == "Airport Inspection Services":
			planned_mission_list = self.mission_manager.accepted_missions["HEATHROW"]
			task_order_list = self.mission_manager.pending_task_orders["HEATHROW"]
		elif self.activities_list.currentItem().text() == "Navaids Inspection Services":
			planned_mission_list = self.mission_manager.accepted_missions["RHODES"]
			task_order_list = self.mission_manager.pending_task_orders["RHODES"]
		elif self.activities_list.currentItem().text() == "Waterdrome Inspection Services":
			planned_mission_list = self.mission_manager.accepted_missions["CORFU"]
			task_order_list = self.mission_manager.pending_task_orders["CORFU"]

		for planned_mission in planned_mission_list:
			planned_mission_widget = PlannedMissionWidget(mission = planned_mission)
			self.planned_inspection_box_layout.addWidget(planned_mission_widget)
			planned_mission_widget.show()

		self.planned_inspection_box_layout.addStretch()

		for task_order in task_order_list:
			task_order_widget = PlannedMissionWidget(task_order = task_order)
			self.planned_inspection_box_layout.addWidget(task_order_widget)
			task_order_widget.show()



	def populate_inspection_planning_box(self, service):
		# add forAll widgets if not already added
		if self.task_order_information_widget_list_forAll[0][0].parentWidget() is None:
			for widget in self.task_order_information_widget_list_forAll:
				self.service_detail_box_layout.addRow(widget[0], widget[1])

		# remove not forAll widgets
		for widget in self.task_order_information_widget_list_custom:
			widget.setParent(None)


	def send_task_order(self):
		# TODO changer tout ça c'est pas du beau code

		if self.activities_list.currentItem().text() == "Airport Inspection Services":
			activity = "AIRPORT_INSPECTION"
			location = "HEATHROW"
			if self.inspection_services_list.currentItem().text() == "Taxiway Apron Inspection":
				service = "TAXIWAY_APRON_INSPECTION"
			elif self.inspection_services_list.currentItem().text() == "Taxiway Lights Inspection":
				service = "TAXIWAY_LIGHT_INSPECTION"
			elif self.inspection_services_list.currentItem().text() == "FOD Detection":
				service = "FOD_DETECTION"
			elif self.inspection_services_list.currentItem().text() == "Perimeter Surveillance":
				service = "PERIMETER_SURVEILLANCE"
			elif self.inspection_services_list.currentItem().text() == "Infrastructure Inspection":
				service = "INFRASTRUCTURE_INSPECTION"

		elif self.activities_list.currentItem().text() == "Navaids Inspection Services":
			activity = "NAVAID_INSPECTION"
			location = "RHODES"
			if self.inspection_services_list.currentItem().text() == "VOR Extended Ground Test":
				service = "VOR_EXTENDED_GROUND_TEST"
			elif self.inspection_services_list.currentItem().text() == "VOR Short Range Flight Test":
				service = "VOR_SHORT_RANGE_FLIGHT_TEST"
			elif self.inspection_services_list.currentItem().text() == "DME DME Evaluation":
				service = "DME_DME_INSPECTION"

		elif self.activities_list.currentItem().text() == "Waterdrome Inspection Services":
			activity = "WATERDROME_INSPECTION"
			location = "CORFU"
			if self.inspection_services_list.currentItem().text() == "Infrastructure Inspection":
				service = "INFRASTRUCTURE_INSPECTION"
			elif self.inspection_services_list.currentItem().text() == "Waterway Inspection":
				service = "WATERWAY_INSPECTION"

		self.mission_manager.create_task_order(
			activity = activity,
			location = location,
			service = service,
			target = self.target_line_edit.text(),
			date = self.date_line_edit.text(),
			time = self.time_line_edit.text())

		# update planned mission window
		self.populate_planned_inspections_box()

		self.mission_manager.comms.new_task_order_signal.emit(location)

		self.hide()
		