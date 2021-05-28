#!/usr/bin/python3

import sys
from os import path, getenv

import geojsonio

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan

from .airmap_request_manager import AirmapRequestManager
from .fint_request_manager import FintRequestManager
from .pprz_request_manager import PprzRequestManager

## This is the main request manager
## This program is in direct link with the UI
## It uses functions from sub request managers

class RequestManager(object):

	def __init__(self):
		super().__init__()
		## initiate ivy interface 
		self.interface = IvyMessagesInterface("msgInterface")
		## sub request managers instanciation 
		self.airmap_request_manager = AirmapRequestManager()
		self.fint_request_manager = FintRequestManager()
		self.pprz_request_manager = PprzRequestManager(self.interface)
		## initiate interface subscriptions
		## update_config updates the flight plan and the flight plan geojson geometry
		self.pprzconnect = PprzConnect(notify=self.pprz_request_manager.update_config, ivy=self.interface)

	def log_in_to_airmap_API(self, client_id, user_name, password, connection_status_label):
		# retreives the authentification information provided in the UI by the user and updates the airmap user profile
		self.airmap_request_manager.update_credentials(client_id, user_name, password)
		# request token to airmap API, stores it in the airmap user profile and updates the connection status label given in argument
		# the token has to be refreshed regularly, so a thread is also created to take care of this refresh
		self.airmap_request_manager.log_in(connection_status_label)
		# retreives the pilot profile information and the pilot's aircrafts and stores them in the airmap user profile
		self.airmap_request_manager.get_user_information()


	def log_in_to_fint_API(self, user_name, password, connection_status_label):
		# retreives the authentification information provided in the UI by the user and updates the fint user profile
		self.fint_request_manager.update_credentials(user_name, password)
		# request token to FINT API, stores it in the FINT user profile and updates the connection status label given in argument
		# the token has to be refreshed regularly, so a thread is also created to take care of this refresh
		self.fint_request_manager.log_in(connection_status_label)

	def send_flight_plan_to_airmap(self, flight_plan_confirmation_window):
		flight_plan = self.pprz_request_manager.flight_plan
		if self.pprz_request_manager.fl_geojson is None:
			self.pprz_request_manager.convert_flight_plan_to_geojson()
		flight_plan_geometry = self.pprz_request_manager.fl_geojson
		# creates the flight plan with airmap's formalism
		self.airmap_request_manager.create_flight_plan(flight_plan_geometry, flight_plan.lat0, flight_plan.lon0)
		# popup to confirm the flight plan information before it is sent to airmap
		# /!\ not finished /!\
		# geojsonio.display(flight_plan_geometry)
		# confirmation_popup.exec()
		flight_plan_confirmation_window.exec_()
		# if flight_plan_confirmation_window.exec_() == QDialog.Accepted:
		# submits flight plan to airmap
		self.airmap_request_manager.submit_flight_plan()
		# shows the geometry of the flight plan sent on pprz GCS / this is optional /!\ TODO implement this "optionnality" 
		self.pprz_request_manager.show_geojson_flight_plan()

	def show_all_surrounding_airspaces(self):
		# retreives the mission area of the flight plan / this is a square the size of the max_dist_from_home argument of the flight plan
		mission_area = self.pprz_request_manager.get_mission_area()
		# retreives the airspaces included in this mission area
		airspaces = self.airmap_request_manager.get_airspaces_in_geometry(mission_area)
		if airspaces is None:
			print("No airspaces in mission area")
			return
		# shows the airspaces on pprz GCS
		self.pprz_request_manager.send_pprzShapeMessage_from_GeoJSON(airspaces)
		return

	def show_intersecting_airspaces(self):
		if self.pprz_request_manager.fl_geojson is None:
			self.pprz_request_manager.convert_flight_plan_to_geojson()
		# retreives the flight plan geometry
		flight_plan_geometry = self.pprz_request_manager.fl_geojson
		# retreives the airspaces included in this mission area
		airspaces = self.airmap_request_manager.get_airspaces_in_geometry(flight_plan_geometry)
		if airspaces is None:
			print("No airspaces in flight plan geometry")
			return
		# shows the airspaces on pprz GCS
		self.pprz_request_manager.send_pprzShapeMessage_from_GeoJSON(airspaces)
		return