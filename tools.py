## tools to be used in py files in pprz_5D

import math

import sys
import requests
from os import path, getenv
import json

# PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.join(path.dirname(
# 	path.abspath(__file__)), '..')))
PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(
	path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage

## tools for the coordinates

def dms_to_deg(dms):
	coord = dms.split(" ")
	d = float(coord[0])
	min = float(coord[1])
	sec = float(coord[2])
	degrees = d + (min/60) + (sec/3600)
	return degrees

def add_lat_and_meters(deg_lat, m):
	new_lat = deg_lat + (m / 6378000) * (180 / math.pi)
	return float("%.6f" % new_lat)

def add_lon_and_meters(deg_lon, deg_lat, m):
	new_lon = deg_lon + (m / 6378000) * (180 / math.pi) / math.cos(deg_lat * math.pi / 180)
	return float("%.6f" % new_lon)

def sub_lat_and_meters(deg_lat, m):
	new_lat = deg_lat - (m / 6378000) * (180 / math.pi)
	return float("%.6f" % new_lat)

def sub_lon_and_meters(deg_lon, deg_lat, m):
	new_lon = deg_lon - (m / 6378000) * (180 / math.pi) / math.cos(deg_lat * math.pi / 180)
	return float("%.6f" % new_lon)

## function to extract data from GeoJSON object in order to create a PprzMessage
def pprzShapeMessage_from_GeoJSON(geo):
	msg_list = []
	id_number = 0
	## fills an already existing PprzMessage with information from the GeoJSON
	if geo['status'] == 'success':
		for area in geo['data']:
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
			msg_list.append(msg_shape)
	else:
		print ('failure in retrieving airspaces')
	return(msg_list)

def generate_geojson_from_xml(xml_file):
	# potential function for generation of more precise geoJSON geometry to define flight plan
	return 0
