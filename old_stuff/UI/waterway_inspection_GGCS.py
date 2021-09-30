#!/usr/bin/python3

from .custom_widgets.out_log import OutLog

import sys
from PySide6 import QtCore, QtWidgets, QtGui

import pyqtgraph

class WaterwayInspectionGGCS(QtWidgets.QWidget):

	def __init__(self, req_manager):
		super().__init__()
		self.request_manager = req_manager

		# UI layout init
		self.setWindowTitle("Waterway Inspection GGCS")
		self.main_layout = QtWidgets.QHBoxLayout(self)
		self.left_v_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.left_v_layout)
		self.right_v_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addLayout(self.right_v_layout)
		self.left_top_h_layout = QtWidgets.QHBoxLayout()
		self.left_v_layout.addLayout(self.left_top_h_layout)

		#add boxes, view and out log
		self.box_flight_states = QtWidgets.QGroupBox("Flight States")
		self.box_flight_states.setFixedWidth(400)
		self.left_top_h_layout.addWidget(self.box_flight_states)
		self.graphWidget = pyqtgraph.PlotWidget()
		self.left_top_h_layout.addWidget(self.graphWidget)
		self.out_log = QtWidgets.QTextEdit()
		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.out_log.setFont(self.font)
		self.out_log.setFixedHeight(200)
		self.left_v_layout.addWidget(self.out_log)
		sys.stdout = OutLog(self.out_log, sys.stdout)
		self.box_coordination = QtWidgets.QGroupBox("Coordination")
		self.box_coordination.setFixedWidth(400)
		self.right_v_layout.addWidget(self.box_coordination)
		self.box_payload = QtWidgets.QGroupBox("Payload Information")
		self.right_v_layout.addWidget(self.box_payload)

		# view setup
		self.graphWidget.showGrid(x = True, y = True, alpha = 0.3) 

		# display flight plans elements


		# connect to FINT and AM APIs
		# self.log_in_to_fint_API()
		# self.log_in_to_airmap_API()

	def log_in_to_airmap_API(self):
		self.request_manager.log_in_to_airmap_API_with_default_cred()

	def log_in_to_fint_API(self):
		self.request_manager.log_in_to_fint_API_with_default_cred()

	def populate_viewer(self):
		flight_plan = self.request_manager.pprz_request_manager.flight_plan
		self.request_manager.pprz_request_manager.convert_flight_plan_to_geojson()
		flight_plan_geometry = self.request_manager.pprz_request_manager.fl_geojson
		wp_list = self.request_manager.pprz_request_manager.wp_list

