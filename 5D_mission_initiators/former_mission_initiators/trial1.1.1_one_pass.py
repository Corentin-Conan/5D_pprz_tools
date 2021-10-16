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

def trial1_1_1_one_pass_init():


	flight_plan = None
	wp_list = None

	wp_names = ["STDBY", "stand_1", "stand_2", "stand_3", "stand_4", "tax_1", "tax_2", "TD"]
	# wp_names = ["STDBY", "stand_1", "stand_2", "stand_3"]	
	wp_list = []
	sorted_wp_list = []



	def sort_like(list_to_sort, list_model):
		if not len(list_to_sort) == len(list_model):
			print("lists not same size")
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
		msg_mv_wp["ac_id"] = 41
		msg_mv_wp["lon"] = int(coord[0] * 10000000)
		msg_mv_wp["lat"] = int(coord[1] * 10000000)
		msg_mv_wp["alt"] = 150000
		print(msg_mv_wp)
		interface.send(msg_mv_wp)


	# called when pprz is running
	def update_config(config):
		pass

		print("update config")

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
			buffer_cont = line_full_path.buffer(0.00025, resolution = 1, cap_style = 1, join_style = 1)

			# show_shape_on_gcs(buffer_cont.exterior.coords, 1, "red")

			id = 11

			for coord in buffer_cont.exterior.coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			interface.unsubscribe_all()

			return



	interface = IvyMessagesInterface("msgInterface")
	pprzconnect = PprzConnect(notify=update_config, ivy=interface)
	interface.subscribe(update_wp_list, PprzMessage("ground", "WAYPOINT_MOVED"))

	msg_shape = PprzMessage("ground", "SHAPE")
	msg_shape['id'] = 3
	msg_shape['linecolor'] = "red"
	msg_shape['fillcolor'] = "red"
	msg_shape['opacity'] = 1
	msg_shape['shape'] = 1
	msg_shape['status'] = 0 
	lonarr = [51.468974, 51.468974, 51.468559, 51.468559, 51.467916, 51.467916, 51.467661, 51.467538, 51.467573, 51.467687, 51.467887, 51.467878, 51.467672, 51.467880, 51.467887, 51.467694, 51.467566, 51.467550, 51.467616, 51.467694, 51.467145, 51.467252, 51.467318, 51.467259, 51.467129, 51.466968, 51.466968, 51.467075, 51.467197, 51.467290, 51.467164, 51.466973, 51.466973, 51.467115, 51.467282, 51.467242, 51.467127, 51.466959, 51.466959, 51.467890, 51.467913, 51.468542, 51.468542]
	latarr = [-0.489199, -0.485307, -0.485311, -0.487162, -0.487162, -0.487351, -0.487283, -0.487097, -0.485663, -0.485072, -0.484950, -0.484358, -0.484101, -0.483854, -0.483262, -0.483133, -0.482447, -0.480459, -0.479450, -0.479093, -0.479093, -0.479416, -0.480345, -0.481271, -0.481707, -0.481825, -0.482458, -0.482492, -0.482731, -0.483391, -0.484157, -0.484358, -0.485003, -0.485094, -0.486024, -0.486593, -0.487036, -0.487158, -0.487632, -0.487632, -0.487833, -0.487833, -0.489199]
	for i in range(len(lonarr)):
		lonarr[i] *= 10000000
		lonarr[i] = int(lonarr[i])
	for i in range(len(latarr)):
		latarr[i] *= 10000000
		latarr[i] = int(latarr[i])
	msg_shape['latarr'] = lonarr
	msg_shape['lonarr'] = latarr
	msg_shape['text'] = "area_23"
	print(msg_shape)
	interface.send(msg_shape)




def main():
	trial1_1_1_one_pass_init()

if __name__ == '__main__':
	main()