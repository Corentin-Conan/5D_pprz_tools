#!/usr/bin/python3

import sys
from os import path, getenv

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")
sys.path.append(PPRZ_HOME + "/5D_API/toolkit")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan

from flight_plan_tools import *
from waypoint import Waypoint

class PprzRequestManager(object):

	def __init__(self, interface):
		super().__init__()
		self.flight_plan = None
		self.fl_geojson = None
		self.interface = interface
		self.wp_list = []
		self.interface.subscribe(self.update_wp_list, PprzMessage("ground", "WAYPOINT_MOVED"))

	def update_config(self, config):
		print("update config")
		self.flight_plan = FlightPlan.parse(config.flight_plan)
		# for wp in self.flight_plan.waypoints:
		# 	print(wp.lon)
		# 	print(wp.lat)
		# 	print(wp.name)

	def update_wp_list(self, msg_id, msg):
		wp = Waypoint(msg["wp_id"], None, None, None, msg["lat"], msg["long"], msg["alt"], msg["ground_alt"])
		is_already_in_wp_list = False
		for current_wp in self.wp_list:
			if wp.id == current_wp.id:
				is_already_in_wp_list = True
				wp.lat = msg["lat"]
				wp.lon = msg["lon"]
				wp.alt = msg["lat"]
				wp.ground_alt = msg["ground_alt"]
		if not is_already_in_wp_list:
			self.wp_list.append(wp)
		# print(self.wp_list)

	def convert_flight_plan_to_geojson(self):
		if self.flight_plan is not None:
			self.fl_geojson = pprz_flight_plan_to_geojson(self.wp_list, d_buffer = 0.001)
		else:
			print("No flight plan to convert")

	def send_flight_plan_to_airmap(self):
		## TODO ##
		return(0)

	def show_geojson_flight_plan(self):
		if self.fl_geojson is not None:
			lat0 = dms_to_deg(self.flight_plan.lat0)
			lon0 = dms_to_deg(self.flight_plan.lon0)
			msg = PprzMessage("ground", "SHAPE")
			msg['id'] = 1
			msg['linecolor'] = 'red'
			msg['fillcolor'] = 'red'
			msg['opacity'] = 1
			msg['shape'] = 1
			msg['status'] = 0
			latarr = []
			lonarr = []
			for coord in self.fl_geojson['coordinates'][0]:
				# latarr.append(int(add_lat_and_meters(lat0, coord[0]) * 10000000))
				# lonarr.append(int(add_lon_and_meters(lon0, lat0, coord[1]) * 10000000))
				latarr.append(int(coord[0] * 10000000))
				lonarr.append(int(coord[1] * 10000000))
			msg['latarr'] = latarr
			msg['lonarr'] = lonarr
			msg['text'] = 'buffer'
			print('sending message : ' + str(msg))
			self.interface.send(msg)
		else:
			print("Geojson flight plan not defined")