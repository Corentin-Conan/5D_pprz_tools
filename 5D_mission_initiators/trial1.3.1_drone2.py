#!/usr/bin/python3

import sys
from os import path, getenv
import time

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan, Waypoint

import shapely.geometry


def trial1_2_1_init():

	# one day maybe start pprz with correct aircraft and flight plan from here

	flight_plan = None
	wp_list = None

	# params for sector definition
	# sect_1_wp_names = ["O.M_70", "I.M_70", "WP12", "WP11", "WP10", "WP9"]
	sect_1_wp_names = ["O.M_70", "I.M_70", "WP12", "WP11", "WP10", "WP9"]
	sect_1_wp = []
	sorted_sect_1_wp = []

	sect_2_wp_names = ["I.M_250", "WP2", "WP3", "WP4", "WP5"]
	sect_2_wp = []
	sorted_sect_2_wp = []

	sect_3_wp_names = ["STDBY", "I.M_250"]
	sect_3_wp = []
	sorted_sect_3_wp = []

	sect_4_wp_names = ["WP5", "WP6", "WP7", "WP8", "WP9"]
	sect_4_wp = []
	sorted_sect_4_wp = []

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

		if int(config.id) == 103:

			# get flight plan
			flight_plan = FlightPlan.parse(config.flight_plan)

			# get flight plan and define params for the operation (eg the waypoint for the diff sectors)
			wp_list = flight_plan.waypoints

			for wp in wp_list:
				print(wp.name)
				if wp.name in sect_1_wp_names:
					sect_1_wp.append(wp)
				if wp.name in sect_2_wp_names:
					sect_2_wp.append(wp)
				if wp.name in sect_3_wp_names:
					sect_3_wp.append(wp)
				if wp.name in sect_4_wp_names:
					sect_4_wp.append(wp)


	def move_wp(wp_id, coord):
		msg_mv_wp = PprzMessage("datalink", "MOVE_WP")
		msg_mv_wp["wp_id"] = wp_id
		msg_mv_wp["ac_id"] = 103
		msg_mv_wp["lon"] = int(coord[0] * 10000000)
		msg_mv_wp["lat"] = int(coord[1] * 10000000)
		msg_mv_wp["alt"] = 150000
		print(msg_mv_wp)
		interface.send(msg_mv_wp)


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
		msg_shape['text'] = "sector"
		print(msg_shape)
		interface.send(msg_shape)


	# function meant to update wp in different sector lists to get their lon and lat
	def update_wp_list(msg_id, msg):

		wp = Waypoint(None, None, None, msg["lat"], msg["long"], msg["alt"], msg["ground_alt"], msg["wp_id"])

		# sect 1
		for current_wp in sect_1_wp:
			if int(wp.no) == int(current_wp.no):
				current_wp.lat = msg["lat"]
				current_wp.lon = msg["long"]
				current_wp.alt = msg["alt"]
				current_wp.ground_alt = msg["ground_alt"]

		sorted_sect_1_wp = sort_like(sect_1_wp, sect_1_wp_names)

		coords_sect_1 = [(wp.lon, wp.lat) for wp in sorted_sect_1_wp]
		print("COORDS SECT 1 : " + str(coords_sect_1))

		# sect 2
		for current_wp in sect_2_wp:
			if int(wp.no) == int(current_wp.no):
				current_wp.lat = msg["lat"]
				current_wp.lon = msg["long"]
				current_wp.alt = msg["alt"]
				current_wp.ground_alt = msg["ground_alt"]

		sorted_sect_2_wp = sort_like(sect_2_wp, sect_2_wp_names)

		coords_sect_2 = [(wp.lon, wp.lat) for wp in sorted_sect_2_wp]
		print("COORDS SECT 2 : " + str(coords_sect_2))

		# sect 3
		for current_wp in sect_3_wp:
			if int(wp.no) == int(current_wp.no):
				current_wp.lat = msg["lat"]
				current_wp.lon = msg["long"]
				current_wp.alt = msg["alt"]
				current_wp.ground_alt = msg["ground_alt"]

		sorted_sect_3_wp = sort_like(sect_3_wp, sect_3_wp_names)

		coords_sect_3 = [(wp.lon, wp.lat) for wp in sorted_sect_3_wp]
		print("COORDS SECT 3 : " + str(coords_sect_3))

		# sect 4
		for current_wp in sect_4_wp:
			if int(wp.no) == int(current_wp.no):
				current_wp.lat = msg["lat"]
				current_wp.lon = msg["long"]
				current_wp.alt = msg["alt"]
				current_wp.ground_alt = msg["ground_alt"]

		sorted_sect_4_wp = sort_like(sect_4_wp, sect_4_wp_names)

		coords_sect_4 = [(wp.lon, wp.lat) for wp in sorted_sect_4_wp]
		print("COORDS SECT 4 : " + str(coords_sect_4))

		if (None, None) not in coords_sect_1 and (None, None) not in coords_sect_2 and (None, None) not in coords_sect_3 and (None, None) not in coords_sect_4:

			# should sort here, since here we have the names
			sorted_sect_1_wp = sort_like(sect_1_wp, sect_1_wp_names)
			sorted_sect_2_wp = sort_like(sect_2_wp, sect_2_wp_names)
			sorted_sect_3_wp = sort_like(sect_3_wp, sect_3_wp_names)
			sorted_sect_4_wp = sort_like(sect_4_wp, sect_4_wp_names)

			# sect 1
			line_sect_1 = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_sect_1_wp])
			buffer_sect_1_cont = line_sect_1.buffer(0.0003, resolution = 1, cap_style = 1, join_style = 1)
			buffer_sect_1_emer = line_sect_1.buffer(0.001, resolution = 1, cap_style = 1, join_style = 1)

			buffer_sect_1_cont_coords = list(buffer_sect_1_cont.exterior.coords)
			buffer_sect_1_emer_coords = list(buffer_sect_1_emer.exterior.coords)

			print("sect 1 cont : " + str(buffer_sect_1_cont_coords))
			print("sect 1 emer : " + str(buffer_sect_1_emer_coords))

			show_shape_on_gcs(buffer_sect_1_emer_coords, 2, "red")
			show_shape_on_gcs(buffer_sect_1_cont_coords, 1, "blue")

			# sect 2
			line_sect_2 = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_sect_2_wp])
			buffer_sect_2_cont = line_sect_2.buffer(0.0003, resolution = 1, cap_style = 1, join_style = 1)
			buffer_sect_2_emer = line_sect_2.buffer(0.001, resolution = 1, cap_style = 1, join_style = 1)

			buffer_sect_2_cont_coords = list(buffer_sect_2_cont.exterior.coords)
			buffer_sect_2_emer_coords = list(buffer_sect_2_emer.exterior.coords)

			print("sect 2 cont : " + str(buffer_sect_2_cont_coords))
			print("sect 2 emer : " + str(buffer_sect_2_emer_coords))

			show_shape_on_gcs(buffer_sect_2_emer_coords, 3, "red")
			show_shape_on_gcs(buffer_sect_2_cont_coords, 4, "blue")

			# sect 3
			line_sect_3 = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_sect_3_wp])
			buffer_sect_3_cont = line_sect_3.buffer(0.0003, resolution = 1, cap_style = 1, join_style = 1)
			buffer_sect_3_emer = line_sect_3.buffer(0.001, resolution = 1, cap_style = 1, join_style = 1)

			buffer_sect_3_cont_coords = list(buffer_sect_3_cont.exterior.coords)
			buffer_sect_3_emer_coords = list(buffer_sect_3_emer.exterior.coords)

			print("sect 3 cont : " + str(buffer_sect_3_cont_coords))
			print("sect 3 emer : " + str(buffer_sect_3_emer_coords))

			show_shape_on_gcs(buffer_sect_3_emer_coords, 5, "red")
			show_shape_on_gcs(buffer_sect_3_cont_coords, 6, "blue")

			# sect 4
			line_sect_4 = shapely.geometry.LineString([(float(wp.lon), float(wp.lat)) for wp in sorted_sect_4_wp])
			buffer_sect_4_cont = line_sect_4.buffer(0.0003, resolution = 1, cap_style = 1, join_style = 1)
			buffer_sect_4_emer = line_sect_4.buffer(0.001, resolution = 1, cap_style = 1, join_style = 1)

			buffer_sect_4_cont_coords = list(buffer_sect_4_cont.exterior.coords)
			buffer_sect_4_emer_coords = list(buffer_sect_4_emer.exterior.coords)

			print("sect 4 cont : " + str(buffer_sect_4_cont_coords))
			print("sect 4 emer : " + str(buffer_sect_4_emer_coords))

			show_shape_on_gcs(buffer_sect_4_emer_coords, 7, "red")
			show_shape_on_gcs(buffer_sect_4_cont_coords, 8, "blue")

			id = 29

			for coord in buffer_sect_1_cont_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			for coord in buffer_sect_1_emer_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			for coord in buffer_sect_2_cont_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			for coord in buffer_sect_2_emer_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			for coord in buffer_sect_3_cont_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			for coord in buffer_sect_3_emer_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			for coord in buffer_sect_4_cont_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			for coord in buffer_sect_4_emer_coords[0:-1]:
				move_wp(id, coord)
				id += 1
				time.sleep(0.1)

			print("UNSUBSCRIBE !!!")
			interface.unsubscribe_all()

			return



	interface = IvyMessagesInterface("msgInterface")
	pprzconnect = PprzConnect(notify=update_config, ivy=interface)
	interface.subscribe(update_wp_list, PprzMessage("ground", "WAYPOINT_MOVED"))



def main():
	trial1_2_1_init()

if __name__ == '__main__':
	main()