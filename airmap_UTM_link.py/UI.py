#!/usr/bin/python3

import sys

from PySide6 import QtCore, QtWidgets, QtGui

from outlog import OutLog


class UI(QtWidgets.QWidget):


	def __init__(self, _airmap_request_manager, _pprz_request_manager):

		super().__init__()

		# request managers
		self.airmap_request_manager = _airmap_request_manager
		self.pprz_request_manager = _pprz_request_manager

		# variables to keep for easy access by all components
		self.flight_selected = None

		# UI creation
		self.setWindowTitle("Airmap Information Manager")
		self.resize(1200, 800)
		self._layout = QtWidgets.QVBoxLayout(self)

		# font
		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.setFont(self.font)

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
		self.mid_layout = QtWidgets.QFormLayout(self.mid_group_box)
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
		self.flight_plan_list_box = QtWidgets.QGroupBox('Planned Flights List')
		self.left_layout.addWidget(self.flight_plan_list_box)
		self.flight_plan_list_layout = QtWidgets.QVBoxLayout()
		self.flight_plan_list_box.setLayout(self.flight_plan_list_layout)
		self.flight_plan_list = QtWidgets.QListWidget()
		self.flight_plan_list_layout.addWidget(self.flight_plan_list)
		self.flight_plan_list.itemClicked.connect(self.onListItemClicked)

		self.new_flight_button = QtWidgets.QPushButton("New flight")
		self.new_flight_button.setFixedWidth(150)
		self.new_flight_button.clicked.connect(self.create_new_flight)
		self.flight_plan_list_layout.addWidget(self.new_flight_button)

		# flight information window
		self.label_flight_id = QtWidgets.QLabel("Flight ID : ")
		self.flight_id = QtWidgets.QLabel("")
		self.label_flight_plan_id = QtWidgets.QLabel("Flight Plan ID : ")
		self.flight_plan_id = QtWidgets.QLabel("")
		self.label_pilot_id = QtWidgets.QLabel("Pilot ID : ")
		self.pilot_id = QtWidgets.QLabel("")
		self.label_wps = QtWidgets.QLabel("Waypoints : ")
		self.wps = QtWidgets.QLabel("")
		self.label_sorted_wps = QtWidgets.QLabel("Sorted Waypoints : ")
		self.sorted_wps = QtWidgets.QLineEdit("")

		self.compute_am_flight_plan_button = QtWidgets.QPushButton("Compute AIRMAP Flight Plan")
		self.compute_am_flight_plan_button.setFixedWidth(150)
		self.compute_am_flight_plan_button.clicked.connect(self.compute_airmap_flight_plan)

		self.delete_flight_button = QtWidgets.QPushButton("Delete Flight")
		self.delete_flight_button.setFixedWidth(150)
		self.delete_flight_button.clicked.connect(self.delete_flight)

		self.mid_layout.addRow(self.label_flight_id, self.flight_id)
		self.mid_layout.addRow(self.label_flight_plan_id, self.flight_plan_id)
		self.mid_layout.addRow(self.label_pilot_id, self.pilot_id)
		self.mid_layout.addRow(self.label_wps, self.wps)
		self.mid_layout.addRow(self.label_sorted_wps, self.sorted_wps)
		self.mid_layout.addRow(self.compute_am_flight_plan_button)
		self.mid_layout.addRow(self.delete_flight_button)

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
		self.populate_flight_list()


	def populate_flight_list(self):

		flight_widgets = self.airmap_request_manager.load_flight_plans()

		for widget in flight_widgets:

			item = QtWidgets.QListWidgetItem(self.flight_plan_list)
			self.flight_plan_list.addItem(item)

			item.setSizeHint(widget.minimumSizeHint())

			self.flight_plan_list.setItemWidget(item, widget)


	def update_flight_list(self):

		# delete current list items
		self.flight_plan_list.clear()
		# populate with updated flights
		self.populate_flight_list()


	# list item clicked function
	def onListItemClicked(self, item):

		self.flight_selected = self.flight_plan_list.itemWidget(item)
		print("\nItem clicked : " + self.flight_selected.flight_id)
		self.populate_flight_information_window(self.flight_selected)


	# on flight selected, populate flight information window
	def populate_flight_information_window(self, flight):

		print("\nPopulating flight window with flight : " + flight.flight_id)
		self.flight_id.setText(flight.flight_id)
		self.flight_plan_id.setText(flight.flight_plan_id)
		self.pilot_id.setText(flight.pilot_id)

		wps = self.pprz_request_manager.get_waypoints()

		if wps == -1:

			self.wps.setText("No flight plan loaded")
			self.sorted_wps.setText("No flight plan loaded")

		else:

			wp_names = [wp.name for wp in wps]
			self.wps.setText(str(wp_names))
			self.sorted_wps.setText(str(wp_names))


	# on compute airmap flight plan button clicked
	def compute_airmap_flight_plan(self):

		self.pprz_request_manager.compute_airmap_flight_plan_geometry(self.sorted_wps.text())


	# on create new flight button clicked
	def create_new_flight(self):

		print("\nCreate new flight")


	# on delete flight button clicked
	def delete_flight(self):

		print("\nDelete selected flight")
		self.airmap_request_manager.delete_flight(self.flight_selected.flight_id)
		
		# update flight list
		self.update_flight_list()
