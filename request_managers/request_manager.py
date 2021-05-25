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
		self.pprzconnect = PprzConnect(notify=self.pprz_request_manager.update_config, ivy=self.interface)

	def log_in_to_airmap_API(self, client_id, user_name, password, connection_status_label):
		self.airmap_request_manager.update_credentials(client_id, user_name, password)
		self.airmap_request_manager.log_in(connection_status_label)

	def log_in_to_fint_API(self, user_name, password, connection_status_label):
		self.fint_request_manager.update_credentials(user_name, password)
		self.fint_request_manager.log_in(connection_status_label)

	def send_flight_plan_to_airmap(self):
		self.pprz_request_manager.convert_flight_plan_to_geojson()
		flight_plan = self.pprz_request_manager.fl_geojson
		if flight_plan is None:
			print("No GeoJson flight plan")
			return
		self.airmap_request_manager.submit_flight_plan(flight_plan)
		self.pprz_request_manager.show_geojson_flight_plan()

	def show_all_surrounding_airspaces(self):
		mission_area = self.pprz_request_manager.get_mission_area()
		airspaces = self.airmap_request_manager.get_airspaces_in_geometry(mission_area)
		if airspaces is None:
			print("No airspaces in mission area")
			return
		self.pprz_request_manager.send_pprzShapeMessage_from_GeoJSON(airspaces)
		return

	def show_intersecting_airspaces(self):
		print("not implemented yet")
		return