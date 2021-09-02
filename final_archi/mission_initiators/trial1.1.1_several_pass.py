#!/usr/bin/python3

import sys
from os import path, getenv

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan, Waypoint

import shapely.geometry

def trial1_1_1_init():

	print("smth is happening at least")

	flight_plan = None
	wp_list = None

	wp_names = ["stand_1", "stand_2", "stand_3", "stand_4", "stand_5", "stand_6", "stand_7", "stand_8", "stand_9", "tax_1", "tax_2", "tax_3", "tax_4", "tax_5", "tax_6", "tax_7", "tax_8"]
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



	# called when pprz is running
	def update_config(config):

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
			buffer = line_full_path.buffer(0.0001, resolution = 5, cap_style = 1, join_style = 1)

			show_shape_on_gcs(buffer.exterior.coords, 1, "red")

			print("UNSUBSCRIBE !!!")
			interface.unsubscribe_all()

			return



	interface = IvyMessagesInterface("msgInterface")
	pprzconnect = PprzConnect(notify=update_config, ivy=interface)
	interface.subscribe(update_wp_list, PprzMessage("ground", "WAYPOINT_MOVED"))





def main():
	trial1_1_1_init()

if __name__ == '__main__':
	main()