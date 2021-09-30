#!/usr/bin/python3

import sys
from os import path, getenv
from pprz_airmap_interface import Pprz_UTM_Interface
from pprz_fint_interface import Pprz_FINT_Interface
from mission import Mission
from outlog import OutLog
from PySide6 import QtCore, QtWidgets, QtGui

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan


class GGCS(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()
		#creates the ivy interface (must be unique)
		self.interface = IvyMessagesInterface("msgInterface")

		#creates the pprz_airmap_interface
		self.airmap_interface = Pprz_UTM_Interface(self.interface)

		#creates the fint interface
		self.fint_interface = Pprz_FINT_Interface(self.interface)

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
		self.line_edit_client_id.setText(self.airmap_interface.CLIENT_ID)
		self.label_user_name = QtWidgets.QLabel("User Name")
		self.line_edit_user_name = QtWidgets.QLineEdit()
		self.line_edit_user_name.setText(self.airmap_interface.USER_NAME)
		self.label_password = QtWidgets.QLabel("Password")
		self.line_edit_password = QtWidgets.QLineEdit()
		self.line_edit_password.setText(self.airmap_interface.PASSWORD)
		self.user_info_layout = QtWidgets.QFormLayout()
		self.log_in_button = QtWidgets.QPushButton("Log In")
		self.log_in_button.clicked.connect(self.log_in_to_airmap_API)
		self.print_connexion_details_button = QtWidgets.QPushButton("Print Connexion Details")
		self.print_connexion_details_button.clicked.connect(self.print_airmap_connexion_details)
		self.user_info_box.setLayout(self.user_info_layout)
		self.user_info_layout.addRow(self.label_client_id, self.line_edit_client_id)
		self.user_info_layout.addRow(self.label_user_name, self.line_edit_user_name)
		self.user_info_layout.addRow(self.label_password, self.line_edit_password)
		self.user_info_layout.addRow(self.log_in_button, self.print_connexion_details_button)

		#fint api connexion
		self.label_user_name_fint = QtWidgets.QLabel("User Name")
		self.line_edit_user_name_fint = QtWidgets.QLineEdit()
		self.line_edit_user_name_fint.setText(self.fint_interface.username)
		self.label_password_fint = QtWidgets.QLabel("Password")
		self.line_edit_password_fint = QtWidgets.QLineEdit()
		self.line_edit_password_fint.setText(self.fint_interface.password)
		self.user_info_layout_fint = QtWidgets.QFormLayout()
		self.log_in_button_fint = QtWidgets.QPushButton("Log In")
		self.log_in_button_fint.clicked.connect(self.log_in_to_fint_API)
		self.print_connexion_details_button_fint = QtWidgets.QPushButton("Print Connexion Details")
		self.print_connexion_details_button_fint.clicked.connect(self.print_fint_connexion_details)
		self.fint_connexion_box.setLayout(self.user_info_layout_fint)
		self.user_info_layout_fint.addRow(self.label_user_name_fint, self.line_edit_user_name_fint)
		self.user_info_layout_fint.addRow(self.label_password_fint, self.line_edit_password_fint)
		self.user_info_layout_fint.addRow(self.log_in_button_fint, self.print_connexion_details_button_fint)

		#connexion status
		self.label_airmap = QtWidgets.QLabel("Airmap Connexion Status")
		self.label_airmap_status = QtWidgets.QLabel("Not Connected")
		self.label_airmap_status.setStyleSheet("color: rgb(255,0,0)")
		self.label_fint = QtWidgets.QLabel("FINT Connexion Status")
		self.label_fint_status = QtWidgets.QLabel("Not Connected")
		self.label_fint_status.setStyleSheet("color: rgb(255,0,0)")
		self.connexion_status_layout = QtWidgets.QFormLayout()
		self.connexion_status_box.setLayout(self.connexion_status_layout)
		self.connexion_status_layout.addRow(self.label_airmap, self.label_airmap_status)
		self.connexion_status_layout.addRow(self.label_fint, self.label_fint_status)

		#mission request
		self.get_current_mission_params_button = QtWidgets.QPushButton("Get Mission Parameters")
		self.get_current_mission_params_button.clicked.connect(self.print_current_mission_params)
		self.send_flight_plan_to_airmap_button = QtWidgets.QPushButton("Submit Flight Plan")
		self.send_flight_plan_to_airmap_button.clicked.connect(self.send_flight_plan_to_airmap)
		self.get_advisory_flight_plan_button = QtWidgets.QPushButton("Get Flight Plan Advisory")
		self.get_advisory_flight_plan_button.clicked.connect(self.get_advisory_for_flight_plan)
		self.get_airspaces_button = QtWidgets.QPushButton("Get Airspaces")
		self.get_airspaces_button.clicked.connect(self.get_airspaces)
		self.get_other_flights_button = QtWidgets.QPushButton("Get Other Flights")
		self.get_other_flights_button.clicked.connect(self.get_other_flights)
		self.mission_request_layout = QtWidgets.QVBoxLayout()
		self.mission_request_box.setLayout(self.mission_request_layout)
		self.mission_request_layout.addWidget(self.get_current_mission_params_button)
		self.mission_request_layout.addWidget(self.send_flight_plan_to_airmap_button)
		self.mission_request_layout.addWidget(self.get_advisory_flight_plan_button)
		self.mission_request_layout.addWidget(self.get_airspaces_button)
		self.mission_request_layout.addWidget(self.get_other_flights_button)

		#mission monitoring
		self.start_flight_comms_button = QtWidgets.QPushButton("Start Flight Communications")
		self.start_flight_comms_button.clicked.connect(self.start_flight_comms)
		self.send_telemetry_button = QtWidgets.QPushButton("Send Telemetry")
		self.send_telemetry_button.clicked.connect(self.send_telemetry)
		self.mission_monitoring_layout = QtWidgets.QVBoxLayout()
		self.mission_monitoring_box.setLayout(self.mission_monitoring_layout)
		self.mission_monitoring_layout.addWidget(self.start_flight_comms_button)
		self.mission_monitoring_layout.addWidget(self.send_telemetry_button)

		#finot
		self.send_test_object_button = QtWidgets.QPushButton("Send Test Object")
		self.send_test_object_button.clicked.connect(self.send_test_object)
		self.retreive_test_object_button = QtWidgets.QPushButton("Retreive Test Object")
		self.retreive_test_object_button.clicked.connect(self.retreive_test_object)
		self.remove_test_object_button = QtWidgets.QPushButton("Remove Test Object")
		self.remove_test_object_button.clicked.connect(self.remove_test_object)
		self.start_sending_telemetry_button = QtWidgets.QPushButton("Start Sending Telemetry")
		self.start_sending_telemetry_button.clicked.connect(self.start_sending_tele)
		self.stop_sending_telemetry_button = QtWidgets.QPushButton("Stop Sending Telemetry")
		self.stop_sending_telemetry_button.clicked.connect(self.stop_sending_tele)
		self.finot_layout = QtWidgets.QVBoxLayout()
		self.finot_box.setLayout(self.finot_layout)
		self.finot_layout.addWidget(self.send_test_object_button)
		self.finot_layout.addWidget(self.retreive_test_object_button)
		self.finot_layout.addWidget(self.remove_test_object_button)
		self.finot_layout.addWidget(self.start_sending_telemetry_button)
		self.finot_layout.addWidget(self.stop_sending_telemetry_button)


	def log_in_to_airmap_API(self):
		print("\nLogging in to Airmap")
		log_in_status = self.airmap_interface.log_in(
			self.line_edit_client_id.text(),
			self.line_edit_user_name.text(), 
			self.line_edit_password.text())
		if log_in_status == 1:
			self.label_airmap_status.setText("Connected")
			self.label_airmap_status.setStyleSheet("color: rgb(50,200,50)")
		elif log_in_status == 0:
			self.label_airmap_status.setText("Not Connected")
			self.label_airmap_status.setStyleSheet("color: rgb(255,0,0)")
		

	def print_airmap_connexion_details(self):
		print("\nAirmap connexion details :")
		self.airmap_interface.print_connexion_details()


	def log_in_to_fint_API(self):
		print("\nLogging in to FINT")
		log_in_status = self.fint_interface.log_in(
			self.line_edit_user_name_fint.text(),
			self.line_edit_password_fint.text())
		if log_in_status == 1:
			self.label_fint_status.setText("Connected")
			self.label_fint_status.setStyleSheet("color: rgb(50,200,50)")
		elif log_in_status == 0:
			self.label_fint_status.setText("Not Connected")
			self.label_fint_status.setStyleSheet("color: rgb(255,0,0)")


	def print_fint_connexion_details(self):
		print("\nFINT connexion details :")
		self.fint_interface.print_connexion_details()


	def print_current_mission_params(self):
		flight_plan = self.airmap_interface.flight_plan
		if flight_plan is not None:
			print(flight_plan.waypoints)
		else:
			print("No flight plan")


	def send_flight_plan_to_airmap(self):
		print("\nSending flight plan to Airmap")
		flight_plan = self.airmap_interface.flight_plan
		if flight_plan is not None:
			print("Flight Plan Sent")
			self.airmap_interface.create_flight_plan()
		else:
			print("No flight plan")


	def get_advisory_for_flight_plan(self):
		print("\nGetting advisory for flight plan")
		self.airmap_interface.get_advisory_for_flight_plan()


	def get_airspaces(self):
		print("\nGetting airspaces")
		self.airmap_interface.get_UTM_airspace()
		self.airmap_interface.show_UTM_airspace()


	def get_other_flights(self):
		print("\nGetting other flights in airspace")
		self.airmap_interface.get_flights_in_mission_airspace()


	def start_flight_comms(self):
		print("\nStarting flight communications")
		self.airmap_interface.start_flight_comms()


	def send_telemetry(self):
		self.airmap_interface.print_telemetry()


	def send_test_object(self):
		print("\nSending test object to FINT")
		self.fint_interface.send_test_object()


	def retreive_test_object(self):
		print("\nRetreiving test object from FINT")
		self.fint_interface.retreive_test_object()


	def remove_test_object(self):
		print("\nRemoving test object from FINT")
		self.fint_interface.remove_test_object()


	def start_sending_tele(self):
		print("\nSending telemetry to FINT")
		self.fint_interface.cond_send_tele = True


	def stop_sending_tele(self):
		print("\nStop sending telemetry to FINT")
		self.fint_interface.cond_send_tele = False



def main():
	app = QtWidgets.QApplication([])
	ggcs = GGCS()
	ggcs.resize(1400, 900)
	ggcs.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()