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
		self.sorted_wp_list = []
		self.mission_area = None
		self.interface.subscribe(self.update_wp_list, PprzMessage("ground", "WAYPOINT_MOVED"))

	def update_config(self, config):
		self.flight_plan = FlightPlan.parse(config.flight_plan)

	def update_wp_list(self, msg_id, msg):
		wp = Waypoint(msg["wp_id"], None, None, None, msg["lat"], msg["long"], msg["alt"], msg["ground_alt"])
		is_already_in_wp_list = False
		for current_wp in self.wp_list:
			if wp.id == current_wp.id:
				is_already_in_wp_list = True
				current_wp.lat = msg["lat"]
				current_wp.lon = msg["long"]
				current_wp.alt = msg["lat"]
				current_wp.ground_alt = msg["ground_alt"]
		if not is_already_in_wp_list:
			self.wp_list.append(wp)
			self.sorted_wp_list = sorted(self.wp_list, key=lambda wp:int(wp.id))

	def convert_flight_plan_to_geojson(self):
		if self.flight_plan is not None:
			self.fl_geojson = pprz_flight_plan_to_geojson(self.sorted_wp_list, d_buffer = 0.001)
		else:
			print("No flight plan to convert")

	def show_geojson_flight_plan(self):
		if self.fl_geojson is not None:
			lat0 = to_deg(self.flight_plan.lat0)
			lon0 = to_deg(self.flight_plan.lon0)
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
				latarr.append(int(coord[1] * 10000000))
				lonarr.append(int(coord[0] * 10000000))
			msg['latarr'] = latarr
			msg['lonarr'] = lonarr
			msg['text'] = 'buffer'
			self.interface.send(msg)
		else:
			print("Geojson flight plan not defined")

	def get_mission_area(self):
		max_dist = float(self.flight_plan.max_dist_from_home)
		lat0 = float(to_deg(self.flight_plan.lat0))
		lon0 = float(to_deg(self.flight_plan.lon0))
		mission_area = {"type":"Polygon","coordinates":[[[add_lon_and_meters(lon0, lat0, max_dist), sub_lat_and_meters(lat0, max_dist)],[add_lon_and_meters(lon0, lat0, max_dist),add_lat_and_meters(lat0, max_dist)],[sub_lon_and_meters(lon0, lat0, max_dist), add_lat_and_meters(lat0, max_dist)],[sub_lon_and_meters(lon0, lat0, max_dist), sub_lat_and_meters(lat0, max_dist)], [add_lon_and_meters(lon0, lat0, max_dist),sub_lat_and_meters(lat0, max_dist)]]]}
		return(mission_area)

	## function to extract data from GeoJSON object in order to create a PprzMessage
	def send_pprzShapeMessage_from_GeoJSON(self, geo):
		id_number = 0
		## fills an already existing PprzMessage with information from the GeoJSON
		for area in geo:
			## creates  and fills a new PprzMessage for each area
			msg_shape = PprzMessage("ground", "SHAPE")
			msg_shape['id'] = id_number
			id_number += 1
			## color depending on the type of airspace
			if area['type'] == 'controlled_airspace':
				msg_shape['linecolor'] = 'red'
				msg_shape['fillcolor'] = 'red'
			elif area['type'] == 'airport':
				msg_shape['linecolor'] = 'blue'
				msg_shape['fillcolor'] = 'blue'
			else :
				print('unknown airspace type for area id = ' + str(id_number))
			## opacity / 0 - Transparent, 1 - Light Fill, 2 - Medium Fill, 3 - Opaque
			msg_shape['opacity'] = 1
			## shape / 0 - Circle, 1 - Polygon, 2 - Line, 3 - Text
			if area['geometry']['type'] == 'Polygon':
				msg_shape['shape'] = 1
			elif area['geometry']['type'] == 'MultiPolygon':
				msg_shape['shape'] = 1
			# else:
				# print('unknown shape for area id = ' + str(id_number))
			## status / 0 - Create, 1 - Delete
			msg_shape['status'] = 0
			## lonarr & latarr
			lonarr = []
			latarr = []
			if area['geometry']['type'] == 'MultiPolygon':
				for coordinates in area['geometry']['coordinates'][0][0]:
					# print('coordinates = '+str(coordinates))
					lonarr.append(int(coordinates[0] * 10000000))
					latarr.append(int(coordinates[1] * 10000000))
				msg_shape['latarr'] = latarr
				msg_shape['lonarr'] = lonarr
			elif area['geometry']['type'] == 'Polygon':
				for coordinates in area['geometry']['coordinates'][0]:
					# print('coordinates = '+str(coordinates))
					lonarr.append(int(coordinates[0] * 10000000))
					latarr.append(int(coordinates[1] * 10000000))
				msg_shape['latarr'] = latarr
				msg_shape['lonarr'] = lonarr
			## radius = 0 if not circle
			## text
			msg_shape['text'] = area['name'].replace(" ", "_")
			# print(msg_shape)
			self.interface.send(msg_shape)