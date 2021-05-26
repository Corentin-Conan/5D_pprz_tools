#!/usr/bin/python3

import math
import shapely.geometry
import json
from geojson import Polygon
from geojson_rewind import rewind
import geopy

from matplotlib import pyplot

def pprz_flight_plan_to_geojson(wp_list, d_buffer):
	geojson_geometry = None
	waypoints_coord = []
	for wp in wp_list:
		waypoints_coord.append((float(wp.lon), float(wp.lat)))
	line_string = shapely.geometry.LineString(waypoints_coord)
	buffer = line_string.buffer(d_buffer)
	geojson_geometry = Polygon([[[i,j] for i,j in buffer.exterior.coords]])
	geojson_geometry_rewound = rewind(geojson_geometry)
	return(geojson_geometry_rewound)
	# # for visualisation purposes
	# xs_traj = []
	# ys_traj = []
	# xs_buff = []
	# ys_buff = []
	# for wp in waypoints:
	# 	xs_traj.append(wp[0])
	# 	ys_traj.append(wp[1])
	# for pt in list(buffer.exterior.coords):
	# 	xs_buff.append(pt[0])
	# 	ys_buff.append(pt[1])
	# pyplot.plot(xs_traj, ys_traj, linestyle='dashed')
	# pyplot.plot(xs_buff, ys_buff, linestyle='dashed')
	# pyplot.xlim(43,44)
	# pyplot.ylim(1,2)
	# pyplot.show()

def add_lat_and_meters(deg_lat, m):
	# /!\ this method returns an approximate result, but it is enough for what we use it for /!\
	new_lat = deg_lat + (m / 6378000) * (180 / math.pi)
	return float("%.6f" % new_lat)

def add_lon_and_meters(deg_lon, deg_lat, m):
	# /!\ this method returns an approximate result, but it is enough for what we use it for /!\
	new_lon = deg_lon + (m / 6378000) * (180 / math.pi) / math.cos(deg_lat * math.pi / 180)
	return float("%.6f" % new_lon)

def sub_lat_and_meters(deg_lat, m):
	# /!\ this method returns an approximate result, but it is enough for what we use it for /!\
	new_lat = deg_lat - (m / 6378000) * (180 / math.pi)
	return float("%.6f" % new_lat)

def sub_lon_and_meters(deg_lon, deg_lat, m):
	# /!\ this method returns an approximate result, but it is enough for what we use it for /!\
	new_lon = deg_lon - (m / 6378000) * (180 / math.pi) / math.cos(deg_lat * math.pi / 180)
	return float("%.6f" % new_lon)

def dms_to_deg(dms):
	coord = dms.split(" ")
	d = float(coord[0])
	min = float(coord[1])
	sec = float(coord[2])
	direction = coord[3]
	degrees = d + (min/60) + (sec/3600)
	if direction == 'S' or direction == 'W':
		dd *= -1
	return degrees

def main():
	pprz_flight_plan_to_geojson(None, 0.1)

if __name__ == '__main__':
	main()