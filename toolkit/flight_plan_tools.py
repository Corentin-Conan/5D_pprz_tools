#!/usr/bin/python3

import math
import shapely.geometry
import json
from geojson import Polygon
from geojson_rewind import rewind

from matplotlib import pyplot

def pprz_flight_plan_to_geojson(pprz_flight_plan, d_buffer):
	geojson_geometry = None
	waypoints = [(0, 0), (10, 0), (10, 10), (20, 10), (20, 20)]
	line_string = shapely.geometry.LineString(waypoints)
	buffer = line_string.buffer(d_buffer)
	geojson_geometry = Polygon([[[i,j] for i,j in buffer.exterior.coords]])
	geojson_geometry_rewound = rewind(geojson_geometry)
	return(geojson_geometry_rewound)
	# for visualisation purposes
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
	# pyplot.xlim(-10,30)
	# pyplot.ylim(-10,30)
	# pyplot.show()
	

def main():
	pprz_flight_plan_to_geojson(None, 3)

if __name__ == '__main__':
	main()