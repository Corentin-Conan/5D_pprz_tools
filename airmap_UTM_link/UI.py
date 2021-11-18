#!/usr/bin/python3

import sys
import re

import tools

from PySide6 import QtCore, QtWidgets, QtGui

from outlog import OutLog
from dialogs.flight_deletion_confirmation_dialog import FlightDeletionConfirmationDialog
from dialogs.cancel_flight_creation_confirmation_dialog import CancelFlightCreationConfirmationDialog


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
		self.fp_id = None

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
		self.mid_group_box.setFixedWidth(800)
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
		self.log_in_status_label = QtWidgets.QLabel("Not Connected")
		self.log_in_status_label.setAlignment(QtCore.Qt.AlignCenter)
		self.log_in_status_label.setStyleSheet("color: rgb(255,0,0)")

		self.log_in_layout = QtWidgets.QFormLayout()
		self.login_box.setLayout(self.log_in_layout)
		self.log_in_layout.addRow(self.label_client_id, self.line_edit_client_id)
		self.log_in_layout.addRow(self.label_user_name, self.line_edit_user_name)
		self.log_in_layout.addRow(self.label_password, self.line_edit_password)
		self.log_in_layout.addRow(self.log_in_button, self.log_in_status_label)

		# flight plan list
		self.flight_plan_list_box = QtWidgets.QGroupBox('Planned Flights List')
		self.left_layout.addWidget(self.flight_plan_list_box)
		self.flight_plan_list_layout = QtWidgets.QVBoxLayout()
		self.flight_plan_list_box.setLayout(self.flight_plan_list_layout)
		self.flight_plan_list = QtWidgets.QListWidget()
		self.flight_plan_list_layout.addWidget(self.flight_plan_list)
		self.flight_plan_list.itemClicked.connect(self.onFlightSelected)

		self.new_flight_button = QtWidgets.QPushButton("New flight")
		self.new_flight_button.setFixedWidth(150)
		self.new_flight_button.clicked.connect(self.onCreateFlight)
		self.flight_plan_list_layout.addWidget(self.new_flight_button)

		# right box 
		# airspace information box
		self.airspace_information_box = QtWidgets.QGroupBox("Airspace Information")
		self.right_layout.addWidget(self.airspace_information_box)
		self.airspace_information_layout = QtWidgets.QVBoxLayout(self.airspace_information_box)

		self.get_airspaces_button = QtWidgets.QPushButton("Get Airspaces")
		self.get_airspaces_button.clicked.connect(self.get_airspaces)
		self.airspace_information_layout.addWidget(self.get_airspaces_button)

		self.displayed_airspace_list = QtWidgets.QListWidget()
		self.airspace_information_layout.addWidget(self.displayed_airspace_list)

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


	# ========= STATE CHANGE FUNCTIONS ========= #

	# toolbar functions
	def onButtonAccountClicked(self, s):
		print("click", s)


	def onButtonPilotClicked(self, s):
		print("click", s)


	def onButtonAircraftsClicked(self, s):
		print("click", s)


	# on log in clicked
	def logIn(self):

		completion = self.check_log_in_completion()

		if completion:
			log_in_status = self.airmap_request_manager.log_in_to_airmap_API(
				self.line_edit_client_id.text(),
				self.line_edit_user_name.text(),
				self.line_edit_password.text(),
				self.log_in_status_label)

			if log_in_status == "success":
				self.set_log_in_status_label(status = log_in_status)

				print("User logged in to Airmap API")

				self.flight_plan_list_box.setEnabled(True)

				flights = self.airmap_request_manager.load_flight_plans()
				self.populate_flight_list(flights)

			else:
				print("\nLog in error")
				self.manage_log_in_error(log_in_status)

		else:
			print("\nMissing field for log in")



	# on flight in flight list clicked
	def onFlightSelected(self, item):

		self.flight_selected = self.flight_plan_list.itemWidget(item)

		self.enable_flight_param_window(edit = False)

		self.populate_flight_param_window(self.flight_selected, edit = False)


	# on delete flight button pressed
	def onDeleteFlight(self):

		# dialog to confirm deletion
		confirmation = self.deletion_confirmation_dialog()

		if confirmation:

			print("Deletion confirmed")

			self.airmap_request_manager.delete_flight(self.flight_selected.flight_id)

			tools.erase_in_json("airmap.flights.json", flight_id = self.flight_selected.flight_id)
			
			self.update_flight_list()

			self.clear_flight_param_window()

			self.flight_selected = None

		else:

			print("Deletion rejected")

			return


	# on new flight button pressed
	def onCreateFlight(self):

		self.enable_flight_param_window(edit = True)

		self.flight_plan_path = self.get_pprz_flight_plan_path()

		self.pprz_fp_info = self.pprz_request_manager.open_and_parse(self.flight_plan_path, open_GCS = True)

		self.fill_flight_param_window_from_ppz_flight_plan(self.pprz_fp_info)


	def onCreateFlightPlan(self):

		completion_status = self.check_flight_creation_completion()

		# check if completion statu dict is empty, which means completion
		if not bool(completion_status):

			fp_id, success, error_code = self.create_flight_plan()

			if success:

				self.fp_id = fp_id

				# keeps the fp params but switches from text edits to labels
				self.switch_from_edit_to_view()

				rules = self.airmap_request_manager.get_evaluation_for_flight_plan(fp_id)

				# TO IMPLEMENT #
				self.display_rules(rules)

				# patch flight plan according to rules

				# now allow flight plan submission

				# END TO IMPLEMENT #

			else:

				# manage errors here
				print(error_code)
				return

		else :

			print(completion_status)


	# on cancel flight creation button pressed
	def onCancelFlightCreation(self):

		self.flight_plan_path = None
		self.pprz_fp_info = None

		confirmation = self.cancel_flight_creation_confirmation_dialog()

		if confirmation:

			self.clear_flight_param_window()

		else:

			return


	# on submit flight plan button clicked
	def onSubmitFlightPlan(self):

		flight_id, submit_success, error_code = self.submit_flight_plan(self.fp_id)

		if submit_success:

			tools.write_in_json("airmap.flights.json", self.flight_plan_path, flight_id)

			self.clear_flight_param_window()

			# update flight list to show newly created flight
			self.update_flight_list()

		else :

			print(error_code)



	# ========= UI FUNCTIONS =================== #

	def check_log_in_completion(self):

		completion = True

		client_id = self.line_edit_client_id.text()
		user_name = self.line_edit_user_name.text()
		password = self.line_edit_password.text()

		if client_id == "":
			self.line_edit_client_id.setStyleSheet('''QLineEdit{background-color: orange}''')
			completion = False

		if user_name == "":
			self.line_edit_user_name.setStyleSheet('''QLineEdit{background-color: orange}''')
			completion = False

		if password == "":
			self.line_edit_password.setStyleSheet('''QLineEdit{background-color: orange}''')
			completion = False

		return completion



	def set_log_in_status_label(self, status):

		if status == "success":
			# set all fields white in case some were red because of mistake in log in
			self.line_edit_client_id.setStyleSheet('''QLineEdit{background-color: rgb(255, 255, 255)}''')
			self.line_edit_user_name.setStyleSheet('''QLineEdit{background-color: rgb(255, 255, 255)}''')
			self.line_edit_password.setStyleSheet('''QLineEdit{background-color: rgb(255, 255, 255)}''')

			# set log in status label
			self.log_in_status_label.setStyleSheet("color: rgb(50,200,50)")
			self.log_in_status_label.setText("Connected")



	def populate_flight_list(self, flights):

		for widget in flights:

			item = QtWidgets.QListWidgetItem(self.flight_plan_list)
			self.flight_plan_list.addItem(item)

			item.setSizeHint(widget.minimumSizeHint())

			self.flight_plan_list.setItemWidget(item, widget)



	def manage_log_in_error(self, status_code):

		print(status_code)



	def switch_from_edit_to_view(self):

			# get current information
			flight_plan_id = self.fp_id
			pilot_id = self.airmap_request_manager.pilot_id
			start_time = self.start_time.text()
			end_time = self.end_time.text()
			take_off_lat = self.take_off_lat.text()
			take_off_lon = self.take_off_lon.text()
			min_alt_agl = self.min_alt_agl.text()
			max_alt_agl = self.max_alt_agl.text()
			buffer = self.buffer.text()
			flight_description = self.flight_description.text()
			flight_plan_path = self.pprz_flight_plan.text()
			wps = self.wps.text()
			sorted_wps = self.sorted_wps.text()

			self.enable_flight_param_window(edit = False)
			self.delete_flight_button_view_mode.setEnabled(False)
			
			self.flight_id_view_mode.setText("Flight plan not submitted yet")
			self.flight_plan_id_view_mode.setText(flight_plan_id)
			self.pilot_id_view_mode.setText(pilot_id)
			self.start_time_view_mode.setText(start_time)
			self.end_time_view_mode.setText(end_time)
			self.take_off_lat_view_mode.setText(str(take_off_lat))
			self.take_off_lon_view_mode.setText(str(take_off_lon))
			self.min_alt_agl_view_mode.setText(str(min_alt_agl))
			self.max_alt_agl_view_mode.setText(str(max_alt_agl))
			self.buffer_view_mode.setText(str(buffer))
			self.flight_description_view_mode.setText(flight_description)
			self.pprz_flight_plan_view_mode.setText(flight_plan_path)
			self.wps_view_mode.setText(str(wps))
			self.sorted_wps_view_mode.setText(str(wps))



	def enable_flight_param_window(self, edit = True):

		self.mid_group_box.setEnabled(True)

		self.clear_flight_param_window()

		if edit:

			# flight information window == edit mode
			self.label_flight_id = QtWidgets.QLabel("Flight ID : ")
			self.flight_id = QtWidgets.QLabel("")
			self.label_flight_plan_id = QtWidgets.QLabel("Flight Plan ID : ")
			self.flight_plan_id = QtWidgets.QLabel("")
			self.label_pilot_id = QtWidgets.QLabel("Pilot ID : ")
			self.pilot_id = QtWidgets.QLabel("")
			self.label_pprz_flight_plan = QtWidgets.QLabel("Paparazzi flight plan : ")
			self.pprz_flight_plan = QtWidgets.QLabel("")
			# self.change_pprz_flight_plan_button = QtWidgets.QPushButton("Change PPRZ Flight Plan")
			# self.change_pprz_flight_plan_button.setFixedWidth(150)
			# self.change_pprz_flight_plan_button.clicked.connect(self.change_pprz_flight_plan)
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

			# self.compute_am_flight_plan_button = QtWidgets.QPushButton("Compute Flight Geometry")
			# self.compute_am_flight_plan_button.setFixedWidth(150)
			# self.compute_am_flight_plan_button.clicked.connect(self.compute_flight_geometry)

			self.cancel_flight_creation_button = QtWidgets.QPushButton("Cancel Flight Creation")
			self.cancel_flight_creation_button.setFixedWidth(150)
			self.cancel_flight_creation_button.clicked.connect(self.onCancelFlightCreation)

			self.create_flight_plan_button = QtWidgets.QPushButton("Create Flight Plan")
			self.create_flight_plan_button.setFixedWidth(150)
			self.create_flight_plan_button.clicked.connect(self.onCreateFlightPlan)

			self.mid_layout.addRow(self.label_flight_id, self.flight_id)
			self.mid_layout.addRow(self.label_flight_plan_id, self.flight_plan_id)
			self.mid_layout.addRow(self.label_pilot_id, self.pilot_id)
			self.mid_layout.addRow(self.label_pprz_flight_plan, self.pprz_flight_plan)
			# self.mid_layout.addRow(self.change_pprz_flight_plan_button)
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
			# self.mid_layout.addRow(self.compute_am_flight_plan_button)
			self.mid_layout.addRow(self.cancel_flight_creation_button)
			self.mid_layout.addRow(self.create_flight_plan_button)

		else:

			# flight information window == view mode
			self.label_flight_id_view_mode = QtWidgets.QLabel("Flight ID : ")
			self.flight_id_view_mode = QtWidgets.QLabel("")
			self.label_flight_plan_id_view_mode = QtWidgets.QLabel("Flight Plan ID : ")
			self.flight_plan_id_view_mode = QtWidgets.QLabel("")
			self.label_pilot_id_view_mode = QtWidgets.QLabel("Pilot ID : ")
			self.pilot_id_view_mode = QtWidgets.QLabel("")
			self.label_pprz_flight_plan_view_mode = QtWidgets.QLabel("Paparazzi flight plan : ")
			self.pprz_flight_plan_view_mode = QtWidgets.QLabel("")
			# self.change_pprz_flight_plan_button_view_mode = QtWidgets.QPushButton("Change PPRZ Flight Plan")
			# self.change_pprz_flight_plan_button_view_mode.setFixedWidth(150)
			# self.change_pprz_flight_plan_button_view_mode.clicked.connect(self.change_pprz_flight_plan)
			self.label_start_time_view_mode = QtWidgets.QLabel("Start time : ")
			self.start_time_view_mode = QtWidgets.QLabel("YYYY-MM-DDThh:mm:ss.sssZ")
			self.label_end_time_view_mode = QtWidgets.QLabel("End time : ")
			self.end_time_view_mode = QtWidgets.QLabel("YYYY-MM-DDThh:mm:ss.sssZ")
			self.label_take_off_lat_view_mode = QtWidgets.QLabel("Takeoff latitude : ")
			self.take_off_lat_view_mode = QtWidgets.QLabel("")
			self.label_take_off_lon_view_mode = QtWidgets.QLabel("Takeoff longitude : ")
			self.take_off_lon_view_mode = QtWidgets.QLabel("")
			self.label_min_alt_agl_view_mode = QtWidgets.QLabel("Minimum altitude AGL : ")
			self.min_alt_agl_view_mode = QtWidgets.QLabel("0")
			self.label_max_alt_agl_view_mode = QtWidgets.QLabel("Maximum altitude AGL : ")
			self.max_alt_agl_view_mode = QtWidgets.QLabel("")
			self.label_buffer_view_mode = QtWidgets.QLabel("Buffer : ")
			self.buffer_view_mode = QtWidgets.QLabel("")
			self.label_flight_description_view_mode = QtWidgets.QLabel("Flight description : ")
			self.flight_description_view_mode = QtWidgets.QLabel("")

			self.label_wps_view_mode = QtWidgets.QLabel("Waypoints : ")
			self.wps_view_mode = QtWidgets.QLabel("")
			self.label_sorted_wps_view_mode = QtWidgets.QLabel("Sorted Waypoints : ")
			self.sorted_wps_view_mode = QtWidgets.QLabel("")

			# self.compute_am_flight_plan_button_view_mode = QtWidgets.QPushButton("Compute Flight Geometry")
			# self.compute_am_flight_plan_button_view_mode.setFixedWidth(150)
			# self.compute_am_flight_plan_button_view_mode.clicked.connect(self.compute_flight_geometry)

			self.open_fp_in_gcs_button_view_mode = QtWidgets.QPushButton("Open Flight Plan In GCS")
			self.open_fp_in_gcs_button_view_mode.setFixedWidth(150)
			self.open_fp_in_gcs_button_view_mode.clicked.connect(self.open_current_fp)

			self.delete_flight_button_view_mode = QtWidgets.QPushButton("Delete Flight")
			self.delete_flight_button_view_mode.setFixedWidth(150)
			self.delete_flight_button_view_mode.clicked.connect(self.onDeleteFlight)

			self.submit_flight_plan_button = QtWidgets.QPushButton("Submit Flight Plan")
			self.submit_flight_plan_button.setFixedWidth(150)
			self.submit_flight_plan_button.clicked.connect(self.onSubmitFlightPlan)

			self.mid_layout.addRow(self.label_flight_id_view_mode, self.flight_id_view_mode)
			self.mid_layout.addRow(self.label_flight_plan_id_view_mode, self.flight_plan_id_view_mode)
			self.mid_layout.addRow(self.label_pilot_id_view_mode, self.pilot_id_view_mode)
			self.mid_layout.addRow(self.label_pprz_flight_plan_view_mode, self.pprz_flight_plan_view_mode)
			# self.mid_layout.addRow(self.change_pprz_flight_plan_button_view_mode)
			self.mid_layout.addRow(self.open_fp_in_gcs_button_view_mode)
			self.mid_layout.addRow(self.label_start_time_view_mode, self.start_time_view_mode)
			self.mid_layout.addRow(self.label_end_time_view_mode, self.end_time_view_mode)
			self.mid_layout.addRow(self.label_take_off_lat_view_mode, self.take_off_lat_view_mode)
			self.mid_layout.addRow(self.label_take_off_lon_view_mode, self.take_off_lon_view_mode)
			self.mid_layout.addRow(self.label_min_alt_agl_view_mode, self.min_alt_agl_view_mode)
			self.mid_layout.addRow(self.label_max_alt_agl_view_mode, self.max_alt_agl_view_mode)
			self.mid_layout.addRow(self.label_buffer_view_mode, self.buffer_view_mode)
			self.mid_layout.addRow(self.label_flight_description_view_mode, self.flight_description_view_mode)

			self.mid_layout.addRow(self.label_wps_view_mode, self.wps_view_mode)
			self.mid_layout.addRow(self.label_sorted_wps_view_mode, self.sorted_wps_view_mode)
			# self.mid_layout.addRow(self.compute_am_flight_plan_button_view_mode)
			self.mid_layout.addRow(self.delete_flight_button_view_mode)
			self.mid_layout.addRow(self.submit_flight_plan_button)



	def populate_flight_param_window(self, flight, edit = True):

		if edit:

			# print("\nPopulating flight window with flight : " + flight.flight_id)
			self.flight_id.setText(flight.flight_id)
			self.flight_plan_id.setText(flight.flight_plan_id)
			self.pilot_id.setText(flight.pilot_id)
			self.start_time.setText(flight.start_time)
			self.end_time.setText(flight.end_time)
			self.take_off_lat.setText(str(flight.lat))
			self.take_off_lon.setText(str(flight.lon))
			self.min_alt_agl.setText(str(flight.min_altitude))
			self.max_alt_agl.setText(str(flight.max_altitude))
			self.buffer.setText(str(flight.buffer))
			self.flight_description.setText(flight.description)

			pprz_flight_plan_path = tools.get_pprz_fp_path_from_flight_id("airmap.flights.json", flight.flight_id)
			self.flight_plan_path = pprz_flight_plan_path

			self.pprz_fp_info = self.pprz_request_manager.open_and_parse(pprz_flight_plan_path)

			self.pprz_flight_plan.setText(self.flight_plan_path)

			self.take_off_lon.setText(self.pprz_fp_info["lon0"])
			self.take_off_lat.setText(self.pprz_fp_info["lat0"])
			self.max_alt_agl.setText(self.pprz_fp_info["alt"])
			self.wps.setText(str([wp.name for wp in self.pprz_fp_info["waypoints"] if wp.name[0] != "_"]))
			self.sorted_wps.setText(str([wp.name for wp in self.pprz_fp_info["waypoints"] if wp.name[0] != "_"]))

		else :

			# print("\nPopulating flight window with flight : " + flight.flight_id)
			self.flight_id_view_mode.setText(flight.flight_id)
			self.flight_plan_id_view_mode.setText(flight.flight_plan_id)
			self.pilot_id_view_mode.setText(flight.pilot_id)
			self.start_time_view_mode.setText(flight.start_time)
			self.end_time_view_mode.setText(flight.end_time)
			self.take_off_lat_view_mode.setText(str(flight.lat))
			self.take_off_lon_view_mode.setText(str(flight.lon))
			self.min_alt_agl_view_mode.setText(str(flight.min_altitude))
			self.max_alt_agl_view_mode.setText(str(flight.max_altitude))
			self.buffer_view_mode.setText(str(flight.buffer))
			self.flight_description_view_mode.setText(flight.description)

			pprz_flight_plan_path = tools.get_pprz_fp_path_from_flight_id("airmap.flights.json", flight.flight_id)
			self.flight_plan_path = pprz_flight_plan_path

			self.pprz_fp_info = self.pprz_request_manager.open_and_parse(pprz_flight_plan_path)

			self.pprz_flight_plan_view_mode.setText(self.flight_plan_path)

			self.take_off_lon_view_mode.setText(self.pprz_fp_info["lon0"])
			self.take_off_lat_view_mode.setText(self.pprz_fp_info["lat0"])
			self.max_alt_agl_view_mode.setText(self.pprz_fp_info["alt"])
			self.wps_view_mode.setText(str([wp.name for wp in self.pprz_fp_info["waypoints"] if wp.name[0] != "_"]))
			self.sorted_wps_view_mode.setText(str([wp.name for wp in self.pprz_fp_info["waypoints"] if wp.name[0] != "_"]))



	def update_flight_list(self):

		# delete current list items
		self.flight_plan_list.clear()
		# populate with updated flights
		flights = self.airmap_request_manager.load_flight_plans()
		self.populate_flight_list(flights)



	def deletion_confirmation_dialog(self):

		dialog = FlightDeletionConfirmationDialog(self.flight_selected.flight_id)

		if dialog.exec_():
			return True
		else:
			return False



	def clear_flight_param_window(self):
		for i in reversed(range(self.mid_layout.count())): 
			self.mid_layout.itemAt(i).widget().deleteLater()



	def get_pprz_flight_plan_path(self):

		flight_plan_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select flight plan",
			"/home/corentin/paparazzi/conf/flight_plans", "XML Files (*.xml)")[0]
		print(self.flight_plan_path)

		self.pprz_flight_plan.setText(flight_plan_path)

		if flight_plan_path == None:
			return None

		else :
			return flight_plan_path



	def fill_flight_param_window_from_ppz_flight_plan(self, pprz_fp_info):

		print(pprz_fp_info)

		self.take_off_lon.setText(pprz_fp_info["lon0"])
		self.take_off_lat.setText(pprz_fp_info["lat0"])
		self.max_alt_agl.setText(pprz_fp_info["alt"])
		self.wps.setText(str([wp.name for wp in pprz_fp_info["waypoints"] if wp.name[0] != "_"]))
		self.sorted_wps.setText(str([wp.name for wp in pprz_fp_info["waypoints"] if wp.name[0] != "_"]))



	def cancel_flight_creation_confirmation_dialog(self):

		dialog = CancelFlightCreationConfirmationDialog()

		if dialog.exec_():
			return True
		else:
			return False



	def check_flight_creation_completion(self):

		completion_status = {}

		# check all fields against regexps
		# self.end_time // "YYYY-MM-DDThh:mm:ss.sssZ" ou "YYYY-MM-DDThh:mm:ssZ"
		# self.min_alt_agl // [0-9]+\.?[0-9]*
		# self.max_alt_agl // [0-9]+\.?[0-9]*
		# self.buffer // [0-9]+\.?[0-9]*
		# self.flight_description // .*

		iso_date_time_regex = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\\.[0-9]{3})?Z")

		# self.start_time // "YYYY-MM-DDThh:mm:ss.sssZ" ou "YYYY-MM-DDThh:mm:ssZ"
		if self.start_time.text() == "":
			completion_status["start_time"] = "empty"
		elif not iso_date_time_regex.match(self.start_time.text()):
			print("\nSTART TIME DOES NOT MATCH REGEX")
			completion_status["start_time"] = "bad format ; please match YYYY-MM-DDThh:mm:ss.sssZ or YYYY-MM-DDThh:mm:ssZ format"


		return completion_status


	# on create flight plan button clicked
	def create_flight_plan(self):

		self.compute_flight_geometry()

		buffer = self.pprz_request_manager.compute_airmap_flight_plan_geometry(self.pprz_fp_info["waypoints"] ,self.sorted_wps.text())

		fp_id, success, error_code = self.airmap_request_manager.create_flight_plan(None, None,
			self.start_time.text(), self.end_time.text(), None, None,
			self.min_alt_agl.text(), self.max_alt_agl.text(), self.buffer.text(),
			buffer, self.flight_description.text())

		return fp_id, success, error_code


	# on submit flight plan button clicked
	def submit_flight_plan(self, fp_id):

		flight_id, success, error_code = self.airmap_request_manager.submit_flight_plan(fp_id)
		
		return flight_id, success, error_code



	def compute_flight_geometry(self):

		self.pprz_request_manager.get_lat_lon_of_waypoints(self.pprz_fp_info["waypoints"], self.pprz_fp_info["lat0"], self.pprz_fp_info["lon0"])

		self.pprz_request_manager.compute_airmap_flight_plan_geometry(self.pprz_fp_info["waypoints"] ,self.sorted_wps.text())



	# on change pprz flight plan button clicked
	# not used ?? #
	def change_pprz_flight_plan(self):

		self.flight_plan_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select flight plan",
			"/home/corentin/paparazzi/conf/flight_plans", "XML Files (*.xml)")
		print(self.flight_plan_path)

		self.pprz_flight_plan.setText(self.flight_plan_path)



	# on delete flight button clicked
	def delete_flight(self):

		print("\nDelete selected flight")
		self.airmap_request_manager.delete_flight(self.flight_selected.flight_id)

		tools.erase_in_json("airmap.flights.json", flight_id = self.flight_selected.flight_id)
		
		# update flight list
		self.update_flight_list()



	# on get airspaces button clicked
	def get_airspaces(self):

		print("\nRetreiving airspaces")

		mission_geometry = self.pprz_request_manager.get_mission_geometry(self.flight_plan_path)
		
		airspace_type_widgets = self.airmap_request_manager.get_airspaces_in_geometry(mission_geometry)
		
		# self.pprz_request_manager.show_airspaces_on_gcs(airspace_type_widgets)
		
		self.show_airspaces_in_airspace_list(airspace_type_widgets)



	# called on get airspace
	def show_airspaces_in_airspace_list(self, airspace_type_widgets):

		self.displayed_airspace_list.clear()

		for airspace_type_widget in airspace_type_widgets:

			item = QtWidgets.QListWidgetItem(self.displayed_airspace_list)
			self.displayed_airspace_list.addItem(item)
			item.setSizeHint(airspace_type_widget.minimumSizeHint())
			item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)

			self.displayed_airspace_list.setItemWidget(item, airspace_type_widget)



	def open_current_fp(self):

		self.pprz_request_manager.open_current_fp(self.pprz_flight_plan_view_mode.text())



	def get_evaluation_for_flight_plan(self):

		fp_id = self.flight_plan_id_view_mode.text()

		self.airmap_request_manager.get_evaluation_for_flight_plan(fp_id)


	## not used // replaced by get_evaluation_for_flight_plan ##
	def search_for_rulesets(self):

		fp_id = self.flight_plan_id_view_mode.text()

		self.airmap_request_manager.search_for_rulesets(fp_id)



	def display_rules(self, rules):

		advisories = rules.json()["data"]["airspace"]["advisories"]

		for adv in advisories:

			print("\n")
			print(adv)

