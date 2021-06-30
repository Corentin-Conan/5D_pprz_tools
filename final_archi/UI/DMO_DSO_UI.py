#!/usr/bin/python3

from .custom_widgets.out_log import OutLog
from .custom_widgets.planned_mission_widget import PlannedMissionWidget
from .custom_widgets.airspace_widget import AirspaceWidget

import sys
from PySide6 import QtCore, QtWidgets, QtGui

import pyqtgraph

class DMODSOUI(QtWidgets.QWidget):

	def __init__(self, mission_manager, request_manager):
		super().__init__()
	
		self.mission_manager = mission_manager

		self.request_manager = request_manager

		# format airspace : [name, type, x coords, y coords, color]
		self.airspaces_in_location = []

		# subscriptions to signals
		self.mission_manager.comms.new_task_order_signal.connect(self.on_new_task_order)

		self.setWindowTitle("DMO DSO UI - MISSION PLANNING")
		self.resize(1600, 700)

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

		# planned mission box
		self.planned_inspection_box = QtWidgets.QGroupBox("Planned Missions")
		self.h_layout.addWidget(self.planned_inspection_box)
		# self.planned_inspection_box.setFixedWidth(300)

		# task order box
		self.task_order_box = QtWidgets.QGroupBox("Task Order")
		self.task_order_box_layout = QtWidgets.QFormLayout()
		self.task_order_box.setLayout(self.task_order_box_layout)
		self.h_layout.addWidget(self.task_order_box)
		# self.task_order_box.setFixedWidth(200)

		# view
		self.graphWidget = pyqtgraph.PlotWidget()
		self.h_layout.addWidget(self.graphWidget)

		# UTM box 
		self.utm_box = QtWidgets.QGroupBox("UTM Information")
		self.utm_box_layout = QtWidgets.QVBoxLayout()
		self.utm_box.setLayout(self.utm_box_layout)
		self.h_layout.addWidget(self.utm_box)
		self.utm_box.setFixedWidth(300)

		# log in to different APIs
		self.request_manager.log_in_to_airmap_API_with_default_credentials()


	@QtCore.Slot(str)
	def on_new_task_order(self, location):

		self.show()

		# task_order = self.mission_manager.pending_task_orders[location][-1]

		self.populate_planned_mission_window(location)
		self.populate_task_order_window(location)
		self.populate_graphWidget(location)


	def populate_planned_mission_window(self, location):

		planned_mission_list = self.mission_manager.accepted_missions[location]

		self.planned_inspection_box_layout = QtWidgets.QVBoxLayout()
		self.planned_inspection_box.setLayout(self.planned_inspection_box_layout)

		for planned_mission in planned_mission_list:
			planned_mission_widget = PlannedMissionWidget(mission = planned_mission)
			self.planned_inspection_box_layout.addWidget(planned_mission_widget)

		self.planned_inspection_box_layout.addStretch()


	def populate_task_order_window(self, location):

		task_order = self.mission_manager.pending_task_orders[location][-1]

		self.label_activity = QtWidgets.QLabel(task_order.activity)
		self.task_order_box_layout.addWidget(self.label_activity)

		self.label_location = QtWidgets.QLabel(task_order.location)
		self.task_order_box_layout.addWidget(self.label_location)

		self.label_service = QtWidgets.QLabel(task_order.service)
		self.task_order_box_layout.addWidget(self.label_service)

		self.label_target = QtWidgets.QLabel(task_order.target)
		self.task_order_box_layout.addWidget(self.label_target)

		self.label_date = QtWidgets.QLabel("Date : ")
		self.task_order_box_layout.addWidget(self.label_date)
		self.line_edit_date = QtWidgets.QLineEdit()
		self.line_edit_date.setText(task_order.date)
		self.task_order_box_layout.addWidget(self.line_edit_date)

		self.label_time = QtWidgets.QLabel("Time : ")
		self.task_order_box_layout.addWidget(self.label_time)
		self.line_edit_time = QtWidgets.QLineEdit()
		self.line_edit_time.setText(task_order.time)
		self.task_order_box_layout.addWidget(self.line_edit_time)

		self.accept_task_order_button = QtWidgets.QPushButton("Accept Task Order")
		self.task_order_box_layout.addWidget(self.accept_task_order_button)

		self.suggest_modifs_on_task_order_button = QtWidgets.QPushButton("Send Modifications")
		self.task_order_box_layout.addWidget(self.suggest_modifs_on_task_order_button)


	def populate_graphWidget(self, location):

		if location == "HEATHROW":
			flight_area = {"type":"Polygon","coordinates":[[[-0.497573, 51.482516], [-0.497573, 51.457816], [-0.417488, 51.457816], [-0.417488, 51.482516], [-0.497573, 51.482516]]]}

		elif location == "RHODES":
			flight_area = {"type":"Polygon","coordinates":[[[28.046380, 36.411165], [28.046380, 36.391326], [28.114569, 36.391326], [28.114569, 36.411165], [28.046380, 36.411165]]]} 

		elif location == "CORFU":
			flight_area = {"type":"Polygon","coordinates":[[[19.898526, 39.641307], [19.898526, 39.625570], [19.937369, 39.625570], [19.937369, 39.641307], [19.898526, 39.641307]]]}

		# request for flight areas in flight area
		airspaces = self.request_manager.get_airspace_in_geometry(flight_area)
		print(airspaces)

		colors = ['r', 'g', 'b', 'c', 'm', 'y']

		i = 0
		for airspace in airspaces:
			geometry = airspace["geometry"]["coordinates"][0]
			name = airspace["name"]
			type = airspace["type"]
			xs = []
			ys = []
			for elem in geometry:
				xs.append(elem[0])
				ys.append(elem[1])
			self.graphWidget.plot(xs, ys, pen = colors[i%6])
			i+=1
			self.airspaces_in_location.append([name, type, xs, ys, colors[i%6]])

		for airspace in self.airspaces_in_location:
			airspace_widget = AirspaceWidget(airspace)
			self.utm_box_layout.addWidget(airspace_widget)
			self.utm_box_layout.addStretch()


