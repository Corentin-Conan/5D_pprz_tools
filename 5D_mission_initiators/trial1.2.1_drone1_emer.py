#!/usr/bin/python3

import sys
import time
from os import path, getenv

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan, Waypoint

import shapely.geometry

def trial1_2_1_init():

	flight_plan = None
	wp_list = None

	wp_names = ["STDBY", "ENTRY WW4", "OUT WW4", "TD"]
	wp_list = []
	sorted_wp_list = []


	def sort_like(list_to_sort, list_model):
		for wp in list_to_sort:
			print(wp.name)
		if not len(list_to_sort) == len(list_model):
			print("lists not same size")
			print(str(list_to_sort))
			print(str(list_model))
			return
		sorted_list = []
		for elem_model in list_model:
			for elem_to_sort in list_to_sort:
				if elem_to_sort.name == elem_model:
					sorted_list.append(elem_to_sort)
		return sorted_list



	def move_wp(wp_id, coord):
		msg_mv_wp = PprzMessage("datalink", "MOVE_WP")
		msg_mv_wp["wp_id"] = wp_id
		msg_mv_wp["ac_id"] = 4
		msg_mv_wp["lon"] = int(coord[0] * 10000000)
		msg_mv_wp["lat"] = int(coord[1] * 10000000)
		msg_mv_wp["alt"] = 150000
		print(msg_mv_wp)
		interface.send(msg_mv_wp)


	# called when pprz is running
	def update_config(config):

		print("update config")

		if int(config.id) == 4:

			# get flight plan
			flight_plan = FlightPlan.parse(config.flight_plan)

			# get flight plan and define params for the operation (eg the waypoint for the diff sectors)
			wps = flight_plan.waypoints

			for wp in wps:
				if wp.name in wp_names:
					wp_list.append(wp)
					print(wp_list)



	def show_shape_on_gcs(buffer_coords, id, color):
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



	def update_wp_list(msg_id, msg):

		print("update wp list")

		if int(msg.ac_id) == 4:

			wp = Waypoint(None, None, None, msg["lat"], msg["long"], msg["alt"], msg["ground_alt"], msg["wp_id"])

			for current_wp in wp_list:
				if int(wp.no) == int(current_wp.no):
					current_wp.lat = msg["lat"]
					current_wp.lon = msg["long"]
					current_wp.alt = msg["alt"]
					current_wp.ground_alt = msg["ground_alt"]

			sorted_wp_list = sort_like(wp_list, wp_names)

			coords_wp = [(wp.lon, wp.lat) for wp in sorted_wp_list]
			print("COORDS : " + str(coords_wp))

			if (None, None) not in coords_wp:

				line_full_path = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_wp_list])
				buffer_cont = line_full_path.buffer(0.0007, resolution = 1, cap_style = 1, join_style = 1)
				buffer_emer = line_full_path.buffer(0.0011, resolution = 1, cap_style = 1, join_style = 1)
				buffer_limit_kill = line_full_path.buffer(0.0013, resolution = 1, cap_style = 1, join_style = 1)

				buffer_cont_coord = list(buffer_cont.exterior.coords)
				buffer_emer_coord = list(buffer_emer.exterior.coords)
				buffer_limit_kill_coord = list(buffer_limit_kill.exterior.coords)

				show_shape_on_gcs(buffer_limit_kill_coord, 3, "red")
				show_shape_on_gcs(buffer_emer_coord, 2, "orange")
				show_shape_on_gcs(buffer_cont_coord, 1, "green")

				id_1 = 9

				for coord in buffer_cont.exterior.coords[0:-1]:
					move_wp(id_1, coord)
					id_1 += 1
					time.sleep(0.1)

				for coord in buffer_emer.exterior.coords[0:-1]:
					# print("MOVE WP EMER")
					move_wp(id_1, coord)
					id_1 += 1
					time.sleep(0.1)

				interface.unsubscribe_all()

				return



	interface = IvyMessagesInterface("msgInterface")
	pprzconnect = PprzConnect(notify=update_config, ivy=interface)
	interface.subscribe(update_wp_list, PprzMessage("ground", "WAYPOINT_MOVED"))



def main():
	trial1_2_1_init()

if __name__ == '__main__':
	main()