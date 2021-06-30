#!/usr/bin/python3

import sys
from os import path, getenv

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan

from .airmap_request_manager import AirmapRequestManager
# from .fint_request_manager import FintRequestManager
# from .pprz_request_manager import PprzRequestManager

class RequestManager(object):

	def __init__(self):
		super().__init__()
		self.airmap_request_manager = AirmapRequestManager()

	def log_in_to_airmap_API_with_default_credentials(self):
		self.airmap_request_manager.log_in()

	def get_airspace_in_geometry(self, geo):
		airspaces = self.airmap_request_manager.get_airspaces_in_geometry(geo)
		return airspaces



#========================== OLD STUFF =====================================================#


	# def __init__(self):
	# 	super().__init__()
		# initiate ivy interface 
		# self.interface = IvyMessagesInterface("msgInterface")
		## sub request managers instanciation 
		# self.airmap_request_manager = AirmapRequestManager()
		# self.fint_request_manager = FintRequestManager()
		# self.pprz_request_manager = PprzRequestManager(self.interface)
		## initiate interface subscriptions
		## update_config updates the flight plan and the flight plan geojson geometry
		# self.pprzconnect = PprzConnect(notify=self.pprz_request_manager.update_config, ivy=self.interface)

	# def log_in_to_airmap_API(self, client_id, user_name, password, connection_status_label):
	# 	# retreives the authentification information provided in the UI by the user and updates the airmap user profile
	# 	self.airmap_request_manager.update_credentials(client_id, user_name, password)
	# 	# request token to airmap API, stores it in the airmap user profile and updates the connection status label given in argument
	# 	# the token has to be refreshed regularly, so a thread is also created to take care of this refresh
	# 	self.airmap_request_manager.log_in(connection_status_label = connection_status_label)
	# 	# retreives the pilot profile information and the pilot's aircrafts and stores them in the airmap user profile
	# 	self.airmap_request_manager.get_user_information()

	# def log_in_to_airmap_API_with_default_cred(self):
	# 	self.airmap_request_manager.log_in()

	# def log_in_to_fint_API(self, user_name, password, connection_status_label):
	# 	# retreives the authentification information provided in the UI by the user and updates the fint user profile
	# 	self.fint_request_manager.update_credentials(user_name, password)
	# 	# request token to FINT API, stores it in the FINT user profile and updates the connection status label given in argument
	# 	# the token has to be refreshed regularly, so a thread is also created to take care of this refresh
	# 	self.fint_request_manager.log_in(connection_status_label = connection_status_label)

	# def log_in_to_fint_API_with_default_cred(self):
	# 	self.fint_request_manager.log_in()

	# def send_flight_plan_to_airmap(self, flight_plan_confirmation_window):
	# 	# retreives de the pprz flight plan
	# 	flight_plan = self.pprz_request_manager.flight_plan
	# 	# convrets the pprz flight plan to a geojson geometry and stores it in the fl_geojson attribute
	# 	self.pprz_request_manager.convert_flight_plan_to_geojson()
	# 	flight_plan_geometry = self.pprz_request_manager.fl_geojson
	# 	# creates an instance of airmap flight plan with parameters deduced from pprz flight plan
	# 	self.airmap_request_manager.initiate_flight_plan(flight_plan_geometry, flight_plan.lat0, flight_plan.lon0)
	# 	# adds this information on the fp confirmation window
	# 	self.airmap_request_manager.populate_flight_plan_confirmation_window(flight_plan_confirmation_window)
	# 	# show the geojson geometry & waypoints
	# 	wp_list = self.pprz_request_manager.wp_list
	# 	self.airmap_request_manager.show_fp_geometry_on_window(flight_plan_confirmation_window, wp_list)
	# 	# opens the window and blocks the application
	# 	flight_plan_confirmation_window.exec_()
	# 	# don't apply fp modifications if the window has been closed by user
	# 	if flight_plan_confirmation_window.exit_code == 0:
	# 		print("\nFlight plan not sent")
	# 		return
	# 	# updates the airmap flight plan object
	# 	self.airmap_request_manager.update_flight_plan_from_confirmation_window(flight_plan_confirmation_window)
	# 	# creates the flight plan in airmap API
	# 	self.airmap_request_manager.create_flight_plan()
	# 	# submits flight plan to airmap API
	# 	self.airmap_request_manager.submit_flight_plan()
	# 	# shows the geometry of the flight plan sent on pprz GCS / this is optional /!\ TODO implement this "optionnality" 
	# 	self.pprz_request_manager.show_geojson_flight_plan()

	# def show_all_surrounding_airspaces(self):
	# 	# retreives the mission area of the flight plan / this is a square the size of the max_dist_from_home argument of the flight plan
	# 	mission_area = self.pprz_request_manager.get_mission_area()
	# 	# retreives the airspaces included in this mission area
	# 	airspaces = self.airmap_request_manager.get_airspaces_in_geometry(mission_area)
	# 	if airspaces is None:
	# 		print("No airspaces in mission area")
	# 		return
	# 	# shows the airspaces on pprz GCS
	# 	self.pprz_request_manager.send_pprzShapeMessage_from_GeoJSON(airspaces)
	# 	return

	# def show_intersecting_airspaces(self):
	# 	if self.pprz_request_manager.fl_geojson is None:
	# 		self.pprz_request_manager.convert_flight_plan_to_geojson()
	# 	# retreives the flight plan geometry
	# 	flight_plan_geometry = self.pprz_request_manager.fl_geojson
	# 	# retreives the airspaces included in this mission area
	# 	airspaces = self.airmap_request_manager.get_airspaces_in_geometry(flight_plan_geometry)
	# 	if airspaces is None:
	# 		print("No airspaces in flight plan geometry")
	# 		return
	# 	# shows the airspaces on pprz GCS
	# 	self.pprz_request_manager.send_pprzShapeMessage_from_GeoJSON(airspaces)
	# 	return