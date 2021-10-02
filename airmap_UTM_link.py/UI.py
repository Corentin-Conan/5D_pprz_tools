#!/usr/bin/python3

import sys

from PySide6 import QtCore, QtWidgets, QtGui

from outlog import OutLog


class UI(QtWidgets.QWidget):

	def __init__(self, _airmap_request_manager):

		super().__init__()

		self.airmap_request_manager = _airmap_request_manager

		self.setWindowTitle("Airmap Information Manager")
		self.resize(1200, 800)
		self._layout = QtWidgets.QVBoxLayout(self)

		# toolbar
		self.toolbar = QtWidgets.QToolBar("Main Toolbar")
		self._layout.addWidget(self.toolbar)

		self.button_account = QtGui.QAction("Account", self)
		self.button_account.triggered.connect(self.onButtonAccountClicked)
		self.toolbar.addAction(self.button_account)

		self.button_pilot = QtGui.QAction("Pilot", self)
		self.button_pilot.triggered.connect(self.onButtonPilotClicked)
		self.toolbar.addAction(self.button_pilot)

		self.button_aircrafts = QtGui.QAction("Aircrafts", self)
		self.button_aircrafts.triggered.connect(self.onButtonAircraftsClicked)
		self.toolbar.addAction(self.button_aircrafts)

		# main layout
		self.main_box = QtWidgets.QGroupBox('')
		self._layout.addWidget(self.main_box)
		self.main_layout = QtWidgets.QHBoxLayout()
		self.main_box.setLayout(self.main_layout)

		# vertical containers
		self.left_group_box = QtWidgets.QGroupBox('')
		self.left_group_box.setFixedWidth(350)
		self.left_layout = QtWidgets.QVBoxLayout(self.left_group_box)
		self.main_layout.addWidget(self.left_group_box)

		self.mid_group_box = QtWidgets.QGroupBox('')
		self.mid_layout = QtWidgets.QVBoxLayout(self.mid_group_box)
		self.main_layout.addWidget(self.mid_group_box)

		self.right_group_box = QtWidgets.QGroupBox('')
		self.right_layout = QtWidgets.QVBoxLayout(self.right_group_box)
		self.main_layout.addWidget(self.right_group_box)

		## left box widgets
		# login box
		self.login_box = QtWidgets.QGroupBox("Airmap API Connexion")
		self.left_layout.addWidget(self.login_box)
		self.login_box.setFixedHeight(150)

		self.label_client_id = QtWidgets.QLabel("Client ID")
		self.line_edit_client_id = QtWidgets.QLineEdit()
		self.line_edit_client_id.setText(self.airmap_request_manager.client_id)

		self.label_user_name = QtWidgets.QLabel("User Name")
		self.line_edit_user_name = QtWidgets.QLineEdit()
		self.line_edit_user_name.setText(self.airmap_request_manager.user_name)

		self.label_password = QtWidgets.QLabel("Password")
		self.line_edit_password = QtWidgets.QLineEdit()

		self.log_in_button = QtWidgets.QPushButton("Log In")
		self.log_in_button.clicked.connect(self.logIn)
		self.status_label = QtWidgets.QLabel("Not Connected")
		self.status_label.setAlignment(QtCore.Qt.AlignCenter)
		self.status_label.setStyleSheet("color: rgb(255,0,0)")

		self.log_in_layout = QtWidgets.QFormLayout()
		self.login_box.setLayout(self.log_in_layout)
		self.log_in_layout.addRow(self.label_client_id, self.line_edit_client_id)
		self.log_in_layout.addRow(self.label_user_name, self.line_edit_user_name)
		self.log_in_layout.addRow(self.label_password, self.line_edit_password)
		self.log_in_layout.addRow(self.log_in_button, self.status_label)

		# flight plan list
		self.flight_plan_list_box = QtWidgets.QGroupBox('Flight Plan List')
		self.left_layout.addWidget(self.flight_plan_list_box)

		# # main section - information management
		# self.main_box = QtWidgets.QGroupBox("UTM Link")
		# self.main_layout.addWidget(self.main_box)
		# self.main_box_layout = QtWidgets.QHBoxLayout()
		# self.main_box.setLayout(self.main_box_layout)

		# bottom box - outlog
		self.out_log = QtWidgets.QTextEdit()
		self.out_log.setFixedHeight(150)
		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.out_log.setFont(self.font)
		self._layout.addWidget(self.out_log)
		sys.stdout = OutLog(self.out_log, sys.stdout)
		sys.stderr = OutLog(self.out_log, sys.stderr)

	# toolbar functions
	def onButtonAccountClicked(self, s):
		print("click", s)

	def onButtonPilotClicked(self, s):
		print("click", s)

	def onButtonAircraftsClicked(self, s):
		print("click", s)

	# button functions
	def logIn(self):
		self.airmap_request_manager.log_in_to_airmap_API(
			self.line_edit_client_id.text(),
			self.line_edit_user_name.text(),
			self.line_edit_password.text(),
			self.status_label)