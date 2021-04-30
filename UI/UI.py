#!/usr/bin/python3

from .custom_widgets.out_log import OutLog

import sys
from PySide6 import QtCore, QtWidgets, QtGui

class UI(QtWidgets.QWidget):

	def __init__(self, req_manager):
		super().__init__()
		self.request_manager = req_manager

		#UI init
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

		#top boxes
		self.user_info_box = QtWidgets.QGroupBox("Airmap API Connexion")
		self.user_info_box.setFixedHeight(150)
		self.user_info_box.setFixedWidth(600)
		self.fint_connexion_box = QtWidgets.QGroupBox("FINT API Connexion")
		self.fint_connexion_box.setFixedHeight(150)
		self.fint_connexion_box.setFixedWidth(600)
		self.connexion_status_box = QtWidgets.QGroupBox("Connexion Status")
		self.connexion_status_box.setFixedHeight(150)
		self.top_layout.addWidget(self.user_info_box)
		self.top_layout.addWidget(self.fint_connexion_box)
		self.top_layout.addWidget(self.connexion_status_box)

		#bottom boxes
		self.mission_request_box = QtWidgets.QGroupBox("Mission Request")
		self.mission_request_box.setFixedHeight(450)
		self.mission_monitoring_box = QtWidgets.QGroupBox("Mission Monitoring")
		self.mission_monitoring_box.setFixedHeight(450)
		self.finot_box = QtWidgets.QGroupBox("FINoT")
		self.finot_box.setFixedHeight(450)
		self.bot_layout.addWidget(self.mission_request_box)
		self.bot_layout.addWidget(self.mission_monitoring_box)
		self.bot_layout.addWidget(self.finot_box)

		#airmap api connexion
		self.label_client_id = QtWidgets.QLabel("Client ID")
		self.line_edit_client_id = QtWidgets.QLineEdit()
		# self.line_edit_client_id.setText(self.airmap_interface.CLIENT_ID)
		self.label_user_name = QtWidgets.QLabel("User Name")
		self.line_edit_user_name = QtWidgets.QLineEdit()
		# self.line_edit_user_name.setText(self.airmap_interface.USER_NAME)
		self.label_password = QtWidgets.QLabel("Password")
		self.line_edit_password = QtWidgets.QLineEdit()
		# self.line_edit_password.setText(self.airmap_interface.PASSWORD)
		self.user_info_layout = QtWidgets.QFormLayout()
		self.log_in_button = QtWidgets.QPushButton("Log In")
		# self.log_in_button.clicked.connect(self.log_in_to_airmap_API)
		self.print_connexion_details_button = QtWidgets.QPushButton("Print Connexion Details")
		# self.print_connexion_details_button.clicked.connect(self.print_airmap_connexion_details)
		self.user_info_box.setLayout(self.user_info_layout)
		self.user_info_layout.addRow(self.label_client_id, self.line_edit_client_id)
		self.user_info_layout.addRow(self.label_user_name, self.line_edit_user_name)
		self.user_info_layout.addRow(self.label_password, self.line_edit_password)
		self.user_info_layout.addRow(self.log_in_button, self.print_connexion_details_button)

		