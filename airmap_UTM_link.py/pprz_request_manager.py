#!usr/bin/python3

import sys
import time
# from os import path, getenv
import os
import subprocess
import xml.etree.ElementTree as ET
import pyproj

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
		

	def get_lat_lon_of_waypoints(self, waypoints, lat0, lon0):

		utm_crs_list = pyproj.database.query_utm_crs_info(
			datum_name = "WGS 84",
			area_of_interest = pyproj.aoi.AreaOfInterest(
				west_lon_degree = float(lon0),
				south_lat_degree = float(lat0),
				east_lon_degree = float(lon0),
				north_lat_degree = float(lat0)
				)
			)
		print(utm_crs_list)

		utm_crs = pyproj.CRS.from_epsg(utm_crs_list[0].code)
		print(utm_crs)

		# p = pyproj.Proj(proj = "utm", zone = utm_crs, ellps = "WGS84", preserve_units = False)
		p = pyproj.Proj(utm_crs, preserve_units = False)

		x0, y0 = p(lon0, lat0)

		for wp in waypoints:
			x, y = x0 + float(wp.x), y0 + float(wp.y)
			wp.lon, wp.lat = p(x, y, inverse = True)
			print(wp.name + " lon : " + str(wp.lon) + " lat : " + str(wp.lat))


	def compute_airmap_flight_plan_geometry(self, waypoints, sorted_wp_names):

		sorted_wp_list = sort_like(waypoints, sorted_wp_names)
		print(sorted_wp_list)

		for wp in sorted_wp_list:
			print("WP : " + wp.name)

		coords_wp = [(wp.lon, wp.lat) for wp in sorted_wp_list]
		print("COORDS : " + str(coords_wp))

		line_full_path = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_wp_list])
		buffer = line_full_path.buffer(0.0005, resolution = 5, cap_style = 1, join_style = 1)

		show_shape_on_gcs(self.interface, buffer.exterior.coords, 1, "red")

		return(buffer.exterior.coords)


	# called when creating a new flight: opens GCS with selected flight plan 
	# and parses flight plan to get requied informations
	def open_and_parse(self, flight_plan_path):

		pprz_fp_info = {}
		waypoints = []

		# open fp in GCS
		x = subprocess.Popen("/home/corentin/PprzGCS/build/pprzgcs/pprzgcs -f " + flight_plan_path, shell = True)

		# parse and get required fp info
		tree = ET.parse(flight_plan_path)
		root = tree.getroot()
		# print(root.attrib)

		for child in root:
			if child.tag == "waypoints":
				for wp in child:
					# print(wp.tag, wp.attrib)
					waypoint = Waypoint(wp.attrib["name"], wp.attrib["x"], wp.attrib["y"], None, None, None, None, None)
					# print(waypoint.name)
					waypoints.append(waypoint)

		pprz_fp_info["alt"] = root.attrib["alt"]
		pprz_fp_info["lat0"] = root.attrib["lat0"]
		pprz_fp_info["lon0"] = root.attrib["lon0"]
		pprz_fp_info["waypoints"] = waypoints

		return pprz_fp_info