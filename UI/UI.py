#!/usr/bin/python3

from .custom_widgets.out_log import OutLog
from .custom_widgets.flight_plan_confirmation_window import FlightPlanConfirmationWindow

import sys
from PySide6 import QtCore, QtWidgets, QtGui

class UI(QtWidgets.QWidget):

	def __init__(self, req_manager):
		super().__init__()
		self.request_manager = req_manager

		# UI layout init
		self.setWindowTitle("GGCS")
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.top_layout = QtWidgets.QHBoxLayout()
		self.bot_layout = QtWidgets.QHBoxLayout()
		self.main_layout.addLayout(self.top_layout)
		self.main_layout.addLayout(self.bot_layout)
		self.out_log = QtWidgets.QTextEdit()
		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.out_log.setFont(self.font)
		self.main_layout.addWidget(self.out_log)
		sys.stdout = OutLog(self.out_log, sys.stdout)

		# sub windows declaration
		self.flight_plan_confirmation_window = None

		# top boxes
		self.user_info_box = QtWidgets.QGroupBox("Airmap API Connection")
		self.user_info_box.setFixedHeight(150)
		self.user_info_box.setFixedWidth(600)
		self.fint_connection_box = QtWidgets.QGroupBox("FINT API Connection")
		self.fint_connection_box.setFixedHeight(150)
		self.fint_connection_box.setFixedWidth(600)
		self.connection_status_box = QtWidgets.QGroupBox("Connection Status")
		self.connection_status_box.setFixedHeight(150)
		self.top_layout.addWidget(self.user_info_box)
		self.top_layout.addWidget(self.fint_connection_box)
		self.top_layout.addWidget(self.connection_status_box)

		# bottom boxes
		self.mission_request_box = QtWidgets.QGroupBox("Mission Request")
		self.mission_request_box.setFixedHeight(450)
		self.mission_monitoring_box = QtWidgets.QGroupBox("Mission Monitoring")
		self.mission_monitoring_box.setFixedHeight(450)
		self.finot_box = QtWidgets.QGroupBox("FINoT")
		self.finot_box.setFixedHeight(450)
		self.bot_layout.addWidget(self.mission_request_box)
		self.bot_layout.addWidget(self.mission_monitoring_box)
		self.bot_layout.addWidget(self.finot_box)

		# airmap api connection
		self.label_client_id = QtWidgets.QLabel("Client ID")
		self.line_edit_client_id = QtWidgets.QLineEdit()
		self.line_edit_client_id.setText(self.request_manager.airmap_request_manager.airmap_user_profile.client_id)
		self.label_user_name = QtWidgets.QLabel("User Name")
		self.line_edit_user_name = QtWidgets.QLineEdit()
		self.line_edit_user_name.setText(self.request_manager.airmap_request_manager.airmap_user_profile.user_name)
		self.label_password = QtWidgets.QLabel("Password")
		self.line_edit_password = QtWidgets.QLineEdit()
		self.line_edit_password.setText(self.request_manager.airmap_request_manager.airmap_user_profile.password)
		self.user_info_layout = QtWidgets.QFormLayout()
		self.log_in_button = QtWidgets.QPushButton("Log In")
		self.log_in_button.clicked.connect(self.log_in_to_airmap_API)
		self.refresh_connection_button = QtWidgets.QPushButton("Refresh Connection")
		self.user_info_box.setLayout(self.user_info_layout)
		self.user_info_layout.addRow(self.label_client_id, self.line_edit_client_id)
		self.user_info_layout.addRow(self.label_user_name, self.line_edit_user_name)
		self.user_info_layout.addRow(self.label_password, self.line_edit_password)
		self.user_info_layout.addWidget(self.log_in_button)
		self.log_in_button.setFixedWidth(100)

		# fint api connection
		self.label_user_name_fint = QtWidgets.QLabel("User Name")
		self.line_edit_user_name_fint = QtWidgets.QLineEdit()
		self.line_edit_user_name_fint.setText(self.request_manager.fint_request_manager.fint_user_profile.user_name)
		self.label_password_fint = QtWidgets.QLabel("Password")
		self.line_edit_password_fint = QtWidgets.QLineEdit()
		self.line_edit_password_fint.setText(self.request_manager.fint_request_manager.fint_user_profile.password)
		self.user_info_layout_fint = QtWidgets.QFormLayout()
		self.log_in_button_fint = QtWidgets.QPushButton("Log In")
		self.log_in_button_fint.clicked.connect(self.log_in_to_fint_API)
		self.fint_connection_box.setLayout(self.user_info_layout_fint)
		self.user_info_layout_fint.addRow(self.label_user_name_fint, self.line_edit_user_name_fint)
		self.user_info_layout_fint.addRow(self.label_password_fint, self.line_edit_password_fint)
		self.user_info_layout_fint.addWidget(self.log_in_button_fint)
		self.log_in_button_fint.setFixedWidth(100)

		# connection status
		self.label_airmap = QtWidgets.QLabel("Airmap Connection Status")
		self.label_airmap_status = QtWidgets.QLabel("Not Connected")
		self.label_airmap_status.setStyleSheet("color: rgb(255,0,0)")
		self.label_fint = QtWidgets.QLabel("FINT Connection Status")
		self.label_fint_status = QtWidgets.QLabel("Not Connected")
		self.label_fint_status.setStyleSheet("color: rgb(255,0,0)")
		self.connection_status_layout = QtWidgets.QFormLayout()
		self.connection_status_box.setLayout(self.connection_status_layout)
		self.connection_status_layout.addRow(self.label_airmap, self.label_airmap_status)
		self.connection_status_layout.addRow(self.label_fint, self.label_fint_status)

		# mission request / preparation
		self.send_flight_plan_to_airmap_button = QtWidgets.QPushButton('Send Flight Plan')
		self.send_flight_plan_to_airmap_button.clicked.connect(self.send_flight_plan_to_airmap)
		self.show_all_surrounding_airspaces_button = QtWidgets.QPushButton('Show All Airspaces')
		self.show_all_surrounding_airspaces_button.clicked.connect(self.show_all_surrounding_airspaces)
		self.show_intersecting_airspaces_button = QtWidgets.QPushButton('Show Intersecting Airspaces Only')
		self.show_intersecting_airspaces_button.clicked.connect(self.show_intersecting_airspaces)
		self.mission_request_box_layout = QtWidgets.QVBoxLayout()
		self.mission_request_box.setLayout(self.mission_request_box_layout)
		self.mission_request_box_layout.addWidget(self.send_flight_plan_to_airmap_button)
		self.mission_request_box_layout.addWidget(self.show_all_surrounding_airspaces_button)
		self.mission_request_box_layout.addWidget(self.show_intersecting_airspaces_button)

	def log_in_to_airmap_API(self):
		self.request_manager.log_in_to_airmap_API(
			self.line_edit_client_id.text(), 
			self.line_edit_user_name.text(),
			self.line_edit_password.text(),
			self.label_airmap_status)

	def log_in_to_fint_API(self):
		self.request_manager.log_in_to_fint_API(
			self.line_edit_user_name_fint.text(),
			self.line_edit_password_fint.text(),
			self.label_fint_status)

	def send_flight_plan_to_airmap(self):
		self.flight_plan_confirmation_window = FlightPlanConfirmationWindow()
		self.request_manager.send_flight_plan_to_airmap(self.flight_plan_confirmation_window)

	def show_all_surrounding_airspaces(self):
		self.request_manager.show_all_surrounding_airspaces()

	def show_intersecting_airspaces(self):
		self.request_manager.show_intersecting_airspaces()