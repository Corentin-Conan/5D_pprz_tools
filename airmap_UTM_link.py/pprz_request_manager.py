#!usr/bin/python3

import sys
import time
# from os import path, getenv
import os
import subprocess
import xml.etree.ElementTree as ET

PPRZ_HOME = os.getenv("PAPARAZZI_HOME", os.path.normpath(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan, Waypoint

import shapely.geometry



def sort_like(list_to_sort, _list_model):
	# if not len(list_to_sort) == len(list_model):
	# 	print("lists not same size")
	# 	return
	sorted_list = []
	list_model = _list_model.strip('][').split(', ')
	for elem_model in list_model:
		for elem_to_sort in list_to_sort:
			if str(elem_to_sort.name) == str(elem_model.strip("''")):
				sorted_list.append(elem_to_sort)
	return sorted_list


def show_shape_on_gcs(interface, buffer_coords, id, color):
	msg_shape = PprzMessage("ground", "SHAPE")
	msg_shape['id'] = id
	msg_shape['linecolor'] = color
	msg_shape['fillcolor'] = color
	msg_shape['opacity'] = 1
	msg_shape['shape'] = 1
	msg_shape['status'] = 0
	lonarr = []
	latarr = []
	for coord in buffer_coords:
		lonarr.append(int(coord[0] * 10000000))
		latarr.append(int(coord[1] * 10000000))
	msg_shape['latarr'] = latarr
	msg_shape['lonarr'] = lonarr
	msg_shape['text'] = "buffer"
	print(msg_shape)
	interface.send(msg_shape)




class PprzRequestManager():

	def __init__(self):

		self.interface = IvyMessagesInterface("msgInterface")
		self.pprzconnect = PprzConnect(notify=self.update_config, ivy=self.interface)
		
		self.pprz_flight_plan = None

		bind_id = self.interface.subscribe(self.update_wp_list, PprzMessage("ground", "WAYPOINT_MOVED"))


	def update_wp_list(self, msg_id, msg):

		print("update wp list")

		for current_wp in self.pprz_flight_plan.waypoints:

			if int(msg["wp_id"]) == int(current_wp.no) and current_wp.name[0] != "_" and current_wp.lon is None:
				current_wp.lat = msg["lat"]
				current_wp.lon = msg["long"]
				current_wp.alt = msg["alt"]
				current_wp.ground_alt = msg["ground_alt"]

				print("WP updated : " + current_wp.name)

		lons = [wp.lon for wp in self.pprz_flight_plan.waypoints if wp.name[0] != "_"]
		
		time.sleep(0.8)	

		if None not in lons:

			print("UNSUBSCRIBE !!")
			self.interface.unsubscribe_all() # use usubscribe(bind_id)

			return


	def update_config(self, config):

		# if ac id == some id // 
		self.pprz_flight_plan = FlightPlan.parse(config.flight_plan)


	def get_waypoints(self):

		if self.pprz_flight_plan == None:

			print("No flight plan loaded from pprz")
			return(-1)

		else:

			wps = self.pprz_flight_plan.waypoints
			wps_not_hidden = []

			for wp in wps:

				if wp.name[0] != "_":

					wps_not_hidden.append(wp)

			return(wps_not_hidden)



	def compute_airmap_flight_plan_geometry(self, sorted_wp_names):

		sorted_wp_list = sort_like(self.pprz_flight_plan.waypoints, sorted_wp_names)
		print(sorted_wp_list)

		for wp in sorted_wp_list:
			print("WP : " + wp.name)

		coords_wp = [(wp.lon, wp.lat) for wp in sorted_wp_list]
		print("COORDS : " + str(coords_wp))

		line_full_path = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_wp_list])
		buffer = line_full_path.buffer(0.0001, resolution = 5, cap_style = 1, join_style = 1)

		show_shape_on_gcs(self.interface, buffer.exterior.coords, 1, "red")

		return(buffer)


	# called when creating a new flight: opens GCS with selected flight plan 
	# and parses flight plan to get requied informations
	def open_and_parse(self, flight_plan_path):

		pprz_fp_info = {}

		# open fp in GCS
		x = subprocess.Popen("/home/corentin/PprzGCS/build/pprzgcs/pprzgcs -f " + flight_plan_path, shell = True)

		# parse and get required fp info
		tree = ET.parse(flight_plan_path)
		root = tree.getroot()
		print(root.attrib)

		return pprz_fp_info