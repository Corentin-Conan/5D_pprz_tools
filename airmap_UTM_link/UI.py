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
		self.flight_plan_path = None
		self.pprz_fp_info = None

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
		self.right_group_box.setFixedWidth(350)
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
		self.label_pprz_flight_plan = QtWidgets.QLabel("Paparazzi flight plan : ")
		self.pprz_flight_plan = QtWidgets.QLabel("")
		self.change_pprz_flight_plan_button = QtWidgets.QPushButton("Change PPRZ Flight Plan")
		self.change_pprz_flight_plan_button.setFixedWidth(150)
		self.change_pprz_flight_plan_button.clicked.connect(self.change_pprz_flight_plan)
		self.label_start_time = QtWidgets.QLabel("Start time : ")
		self.start_time = QtWidgets.QLineEdit("YYYY-MM-DDThh:mm:ss.sssZ")
		self.label_end_time = QtWidgets.QLabel("End time : ")
		self.end_time = QtWidgets.QLineEdit("YYYY-MM-DDThh:mm:ss.sssZ")
		self.label_take_off_lat = QtWidgets.QLabel("Takeoff latitude : ")
		self.take_off_lat = QtWidgets.QLabel("")
		self.label_take_off_lon = QtWidgets.QLabel("Takeoff longitude : ")
		self.take_off_lon = QtWidgets.QLabel("")
		self.label_min_alt_agl = QtWidgets.QLabel("Minimum altitude AGL : ")
		self.min_alt_agl = QtWidgets.QLineEdit("0")
		self.label_max_alt_agl = QtWidgets.QLabel("Maximum altitude AGL : ")
		self.max_alt_agl = QtWidgets.QLineEdit("")
		self.label_buffer = QtWidgets.QLabel("Buffer : ")
		self.buffer = QtWidgets.QLineEdit("")
		self.label_flight_description = QtWidgets.QLabel("Flight description : ")
		self.flight_description = QtWidgets.QLineEdit("")

		self.label_wps = QtWidgets.QLabel("Waypoints : ")
		self.wps = QtWidgets.QLabel("")
		self.label_sorted_wps = QtWidgets.QLabel("Sorted Waypoints : ")
		self.sorted_wps = QtWidgets.QLineEdit("")

		self.compute_am_flight_plan_button = QtWidgets.QPushButton("Compute Flight Geometry")
		self.compute_am_flight_plan_button.setFixedWidth(150)
		self.compute_am_flight_plan_button.clicked.connect(self.compute_flight_geometry)

		self.delete_flight_button = QtWidgets.QPushButton("Delete Flight")
		self.delete_flight_button.setFixedWidth(150)
		self.delete_flight_button.clicked.connect(self.delete_flight)

		self.submit_flight_plan_button = QtWidgets.QPushButton("Submit Flight Plan")
		self.submit_flight_plan_button.setFixedWidth(150)
		self.submit_flight_plan_button.clicked.connect(self.submit_flight_plan)

		self.mid_layout.addRow(self.label_flight_id, self.flight_id)
		self.mid_layout.addRow(self.label_flight_plan_id, self.flight_plan_id)
		self.mid_layout.addRow(self.label_pilot_id, self.pilot_id)
		self.mid_layout.addRow(self.label_pprz_flight_plan, self.pprz_flight_plan)
		self.mid_layout.addRow(self.change_pprz_flight_plan_button)
		self.mid_layout.addRow(self.label_start_time, self.start_time)
		self.mid_layout.addRow(self.label_end_time, self.end_time)
		self.mid_layout.addRow(self.label_take_off_lat, self.take_off_lat)
		self.mid_layout.addRow(self.label_take_off_lon, self.take_off_lon)
		self.mid_layout.addRow(self.label_min_alt_agl, self.min_alt_agl)
		self.mid_layout.addRow(self.label_max_alt_agl, self.max_alt_agl)
		self.mid_layout.addRow(self.label_buffer, self.buffer)
		self.mid_layout.addRow(self.label_flight_description, self.flight_description)

		self.mid_layout.addRow(self.label_wps, self.wps)
		self.mid_layout.addRow(self.label_sorted_wps, self.sorted_wps)
		self.mid_layout.addRow(self.compute_am_flight_plan_button)
		self.mid_layout.addRow(self.delete_flight_button)
		self.mid_layout.addRow(self.submit_flight_plan_button)

		# right box 
		# airspace information box
		self.airspace_information_box = QtWidgets.QGroupBox("Airspace Information")
		self.right_layout.addWidget(self.airspace_information_box)
		self.airspace_information_layout = QtWidgets.QVBoxLayout(self.airspace_information_box)

		self.get_airspaces_button = QtWidgets.QPushButton("Get Airspaces")
		self.get_airspaces_button.clicked.connect(self.get_airspaces)
		self.airspace_information_layout.addWidget(self.get_airspaces_button)

		# flight status box
		self.flight_status_box = QtWidgets.QGroupBox("Flight Status")
		self.right_layout.addWidget(self.flight_status_box)
		self.flight_status_layout = QtWidgets.QVBoxLayout(self.flight_status_box)

		# bottom box - outlog
		self.out_log = QtWidgets.QTextEdit()
		self.out_log.setFixedHeight(150)
		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.out_log.setFont(self.font)
		self._layout.addWidget(self.out_log)
		sys.stdout = OutLog(self.out_log, sys.stdout)
		sys.stderr = OutLog(self.out_log, sys.stderr)

		# set disable blocks at beginning of app
		self.flight_plan_list_box.setDisabled(True)
		self.mid_group_box.setDisabled(True)


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
		self.flight_plan_list_box.setEnabled(True)
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
		self.mid_group_box.setEnabled(True)

		self.populate_flight_information_window(self.flight_selected)


	# on flight selected, populate flight information window
	def populate_flight_information_window(self, flight):

		print("\nPopulating flight window with flight : " + flight.flight_id)
		self.flight_id.setText(flight.flight_id)
		self.flight_plan_id.setText(flight.flight_plan_id)
		self.pilot_id.setText(flight.pilot_id)
		self.start_time.setText(flight.start_time)
		self.end_time.setText(flight.end_time)
		self.take_off_lat.setText(str(flight.lat))
		self.take_off_lon.setText(str(flight.lon))
		self.max_alt_agl.setText(str(flight.max_altitude))
		self.buffer.setText(str(flight.buffer))
		self.flight_description.setText("not implemented yet // see also for min alt agl")

		wps = self.pprz_request_manager.get_waypoints()

		if wps == -1:

			self.wps.setText("No flight plan loaded")
			self.sorted_wps.setText("No flight plan loaded")

		else:

			wp_names = [wp.name for wp in wps]
			self.wps.setText(str(wp_names))
			self.sorted_wps.setText(str(wp_names))


	# on change pprz flight plan button clicked
	def change_pprz_flight_plan(self):

		self.flight_plan_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select flight plan",
			"/home/corentin/paparazzi/conf/flight_plans", "XML Files (*.xml)")
		print(self.flight_plan_path)

		self.pprz_flight_plan.setText(self.flight_plan_path[0])


	# on compute flight geometry button clicked
	def compute_flight_geometry(self):

		self.pprz_request_manager.get_lat_lon_of_waypoints(self.pprz_fp_info["waypoints"], self.pprz_fp_info["lat0"], self.pprz_fp_info["lon0"])

		self.pprz_request_manager.compute_airmap_flight_plan_geometry(self.pprz_fp_info["waypoints"] ,self.sorted_wps.text())


	# on create new flight button clicked
	def create_new_flight(self):

		print("\nCreate new flight")
		self.flight_plan_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select flight plan",
			"/home/corentin/paparazzi/conf/flight_plans", "XML Files (*.xml)")
		print(self.flight_plan_path)

		if self.flight_plan_path == None:

			return

		self.mid_group_box.setEnabled(True)

		self.pprz_flight_plan.setText(self.flight_plan_path[0])
		self.flight_id.setText("")
		self.flight_plan_id.setText("")
		self.pilot_id.setText("")
		self.start_time.setText("YYYY-MM-DDThh:mm:ss.sssZ")
		self.end_time.setText("YYYY-MM-DDThh:mm:ss.sssZ")
		self.take_off_lat.setText("")
		self.take_off_lon.setText("")
		self.max_alt_agl.setText("")
		self.buffer.setText("")
		self.flight_description.setText("")

		self.pprz_fp_info = self.pprz_request_manager.open_and_parse(self.flight_plan_path[0])
		print(self.pprz_fp_info)

		self.take_off_lon.setText(self.pprz_fp_info["lon0"])
		self.take_off_lat.setText(self.pprz_fp_info["lat0"])
		self.max_alt_agl.setText(self.pprz_fp_info["alt"])
		self.wps.setText(str([wp.name for wp in self.pprz_fp_info["waypoints"] if wp.name[0] != "_"]))
		self.sorted_wps.setText(str([wp.name for wp in self.pprz_fp_info["waypoints"] if wp.name[0] != "_"]))


	# on submit flight plan button clicked
	def submit_flight_plan(self):

		buffer = self.pprz_request_manager.compute_airmap_flight_plan_geometry(self.pprz_fp_info["waypoints"] ,self.sorted_wps.text())

		self.airmap_request_manager.create_flight_plan(None, None,
			self.start_time.text(), self.end_time.text(), None, None,
			self.min_alt_agl.text(), self.max_alt_agl.text(), self.buffer.text(),
			buffer, self.flight_description.text())

		# test for writing in json file
		self.airmap_request_manager.write_in_json(flight_plan_path[0], "test")
		
		# update flight list to show newly created flight
		self.update_flight_list()


	# on delete flight button clicked
	def delete_flight(self):

		print("\nDelete selected flight")
		self.airmap_request_manager.delete_flight(self.flight_selected.flight_id)
		
		# update flight list
		self.update_flight_list()


	# on get airspaces button clicked
	def get_airspaces(self):

		print("\nRetreiving airspaces")
		
		mission_geometry = self.pprz_request_manager.get_mission_geometry(self.flight_plan_path[0])
		
		airspaces = self.airmap_request_manager.get_airspaces_in_geometry(mission_geometry)
		
		self.pprz_request_manager.show_airspaces_on_gcs(airspaces)
		
		self.show_airspaces_in_airspace_list(airspaces)


	# called on get airspace
	def show_airspaces_in_airspace_list(airspaces):

		

		pass