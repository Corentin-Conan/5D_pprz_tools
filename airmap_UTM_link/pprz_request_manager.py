#!usr/bin/python3

import sys
import time
# from os import path, getenv
import os
import json
import subprocess
import xml.etree.ElementTree as ET
import pyproj

import tools

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
		

	def get_lat_lon_of_waypoints(self, waypoints, _lat0, _lon0):

		lat0 = tools.to_deg(_lat0)
		lon0 = tools.to_deg(_lon0)

		utm_crs_list = pyproj.database.query_utm_crs_info(
			datum_name = "WGS 84",
			area_of_interest = pyproj.aoi.AreaOfInterest(
				west_lon_degree = float(lon0),
				south_lat_degree = float(lat0),
				east_lon_degree = float(lon0),
				north_lat_degree = float(lat0)
				)
			)
		# print(utm_crs_list)

		utm_crs = pyproj.CRS.from_epsg(utm_crs_list[0].code)
		# print(utm_crs)

		# p = pyproj.Proj(proj = "utm", zone = utm_crs, ellps = "WGS84", preserve_units = False)
		p = pyproj.Proj(utm_crs, preserve_units = False)

		x0, y0 = p(lon0, lat0)

		for wp in waypoints:
			x, y = x0 + float(wp.x), y0 + float(wp.y)
			wp.lon, wp.lat = p(x, y, inverse = True)
			# print(wp.name + " lon : " + str(wp.lon) + " lat : " + str(wp.lat))


	def compute_airmap_flight_plan_geometry(self, waypoints, sorted_wp_names):

		sorted_wp_list = sort_like(waypoints, sorted_wp_names)
		# print(sorted_wp_list)

		# for wp in sorted_wp_list:
		# 	print("WP : " + wp.name)

		coords_wp = [(wp.lon, wp.lat) for wp in sorted_wp_list]
		# print("COORDS : " + str(coords_wp))

		line_full_path = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_wp_list])
		buffer = line_full_path.buffer(0.0005, resolution = 5, cap_style = 1, join_style = 1)

		show_shape_on_gcs(self.interface, buffer.exterior.coords, 1, "red")

		return(buffer.exterior.coords)


	# called when creating a new flight: opens GCS with selected flight plan 
	# and parses flight plan to get requied informations
	def open_and_parse(self, flight_plan_path, open_GCS = False):

		pprz_fp_info = {}
		waypoints = []

		if open_GCS:
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



	def open_current_fp(self, fp_path):

		x = subprocess.Popen("/home/corentin/PprzGCS/build/pprzgcs/pprzgcs -f " + fp_path, shell = True)



	def get_mission_geometry(self, flight_plan_path):

		tree = ET.parse(flight_plan_path)
		root = tree.getroot()

		_lat0 = root.attrib["lat0"]
		_lon0 = root.attrib["lon0"]

		lat0 = tools.to_deg(_lat0)
		lon0 = tools.to_deg(_lon0)

		max_dist_from_home = root.attrib["max_dist_from_home"]

		utm_crs_list = pyproj.database.query_utm_crs_info(
			datum_name = "WGS 84",
			area_of_interest = pyproj.aoi.AreaOfInterest(
				west_lon_degree = float(lon0),
				south_lat_degree = float(lat0),
				east_lon_degree = float(lon0),
				north_lat_degree = float(lat0)
				)
			)

		utm_crs = pyproj.CRS.from_epsg(utm_crs_list[0].code)

		proj = pyproj.Proj(utm_crs, preserve_units = False)

		x0, y0 = proj(lon0, lat0)

		p1 = (x0 - float(max_dist_from_home), y0 - float(max_dist_from_home))
		p2 = (x0 + float(max_dist_from_home), y0 - float(max_dist_from_home))
		p3 = (x0 + float(max_dist_from_home), y0 + float(max_dist_from_home))
		p4 = (x0 - float(max_dist_from_home), y0 + float(max_dist_from_home))

		p_list = [p1, p2, p3, p4, p1]

		p_list_latlon = [proj(p[0], p[1], inverse = True) for p in p_list]

		geometry = {'type': "Polygon",'coordinates':[[[p[0], p[1]] for p in p_list_latlon]]}

		geojson_geometry = json.dumps(geometry)

		# print(geojson_geometry)
		return geojson_geometry


	# for a list of airspaces
	def show_airspaces_on_gcs(self, airspace_type_widgets):

		# airspace_type_widgets is a list of airspace type widget and their respective children airspace widgets

		msg_list = []
		# print(airspaces)
		## fills a PprzMessage with information from the GeoJSON
		for airspace_type_widget in airspace_type_widgets:
			for airspace in airspace_type_widget.children:
				## creates  and fills a new PprzMessage for each area
				msg_shape = PprzMessage("ground", "SHAPE")
				msg_shape['id'] = airspace.pprz_shape_id
				## color depending on the type of airspace
				if airspace.type == 'controlled_airspace':
					msg_shape['linecolor'] = 'red'
					msg_shape['fillcolor'] = 'red'
				elif airspace.type == 'airport':
					msg_shape['linecolor'] = 'blue'
					msg_shape['fillcolor'] = 'blue'
				else :
					msg_shape['linecolor'] = 'orange'
					msg_shape['fillcolor'] = 'orange'
				## opacity / 0 - Transparent, 1 - Light Fill, 2 - Medium Fill, 3 - Opaque
				msg_shape['opacity'] = 1
				## shape / 0 - Circle, 1 - Polygon, 2 - Line, 3 - Text
				if airspace.geometry_type == 'Polygon':
					msg_shape['shape'] = 1
				elif airspace.geometry_type == 'MultiPolygon':
					msg_shape['shape'] = 1
				else:
					print('unknown shape for area id = ' + str(id_number))
				## status / 0 - Create, 1 - Delete
				if airspace.checkbox.isChecked():
					msg_shape['status'] = 0
				else :
					msg_shape['status'] = 1
				## lonarr & latarr
				lonarr = []
				latarr = []
				if airspace.geometry_type == 'MultiPolygon':
					for coordinates in airspace.coordinates[0][0]:
						# print('coordinates = '+str(coordinates))
						lonarr.append(int(coordinates[0] * 10000000))
						latarr.append(int(coordinates[1] * 10000000))
					msg_shape['latarr'] = latarr
					msg_shape['lonarr'] = lonarr
				elif airspace.geometry_type == 'Polygon':
					for coordinates in airspace.coordinates[0]:
						# print('coordinates = '+str(coordinates))
						lonarr.append(int(coordinates[0] * 10000000))
						latarr.append(int(coordinates[1] * 10000000))
					msg_shape['latarr'] = latarr
					msg_shape['lonarr'] = lonarr
				## radius = 0 if not circle
				## text
				msg_shape['text'] = airspace.name.replace(" ", "_")
				print(msg_shape)
				msg_list.append(msg_shape)
		
		for msg in msg_list:
			self.interface.send(msg)


	# for a single airspace
	def show_airspace_on_gcs(self, airspace):

		## fills a PprzMessage with information from the GeoJSON
		## creates  and fills a new PprzMessage for each area
		msg_shape = PprzMessage("ground", "SHAPE")
		msg_shape['id'] = airspace.pprz_shape_id
		## color depending on the type of airspace
		if airspace.type == 'controlled_airspace':
			msg_shape['linecolor'] = 'red'
			msg_shape['fillcolor'] = 'red'
		elif airspace.type == 'airport':
			msg_shape['linecolor'] = 'blue'
			msg_shape['fillcolor'] = 'blue'
		else :
			msg_shape['linecolor'] = 'orange'
			msg_shape['fillcolor'] = 'orange'
		## opacity / 0 - Transparent, 1 - Light Fill, 2 - Medium Fill, 3 - Opaque
		msg_shape['opacity'] = 1
		## shape / 0 - Circle, 1 - Polygon, 2 - Line, 3 - Text
		if airspace.geometry_type == 'Polygon':
			msg_shape['shape'] = 1
		elif airspace.geometry_type == 'MultiPolygon':
			msg_shape['shape'] = 1
		else:
			print('unknown shape for area id = ' + str(id_number))
		## status / 0 - Create, 1 - Delete
		if airspace.checkbox.isChecked():
			msg_shape['status'] = 0
		else :
			msg_shape['status'] = 1
		## lonarr & latarr
		lonarr = []
		latarr = []
		if airspace.geometry_type == 'MultiPolygon':
			for coordinates in airspace.coordinates[0][0]:
				# print('coordinates = '+str(coordinates))
				lonarr.append(int(coordinates[0] * 10000000))
				latarr.append(int(coordinates[1] * 10000000))
			msg_shape['latarr'] = latarr
			msg_shape['lonarr'] = lonarr
		elif airspace.geometry_type == 'Polygon':
			for coordinates in airspace.coordinates[0]:
				# print('coordinates = '+str(coordinates))
				lonarr.append(int(coordinates[0] * 10000000))
				latarr.append(int(coordinates[1] * 10000000))
			msg_shape['latarr'] = latarr
			msg_shape['lonarr'] = lonarr
		## radius = 0 if not circle
		## text
		msg_shape['text'] = airspace.name.replace(" ", "_")
		print(msg_shape)
		
		self.interface.send(msg_shape)