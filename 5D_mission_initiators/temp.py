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

def update_config(config):
	pass

def main():

	buffer = [(28.07285090975767, 36.39296135747923), (28.07280627071375, 36.392917754457336), (28.070256070713747, 36.39089955445734), (28.070104163903547, 36.39083676311485), (28.064756463903546, 36.39022196311485), (28.06468706835762, 36.390222064155054), (28.060412868357623, 36.390726064155054), (28.060150064155053, 36.39105913164238), (28.06048313164238, 36.39132193584495), (28.064722639752027, 36.390822026601754), (28.06995073955724, 36.391423076728024), (28.072409330013013, 36.393368777950606), (28.074811290242334, 36.39626164252077), (28.075233742520766, 36.39630080975767), (28.07527290975767, 36.39587835747923), (28.07285090975767, 36.39296135747923)]
	id = 1
	color = 'red'

	interface = IvyMessagesInterface("msgInterface")
	pprzconnect = PprzConnect(notify=update_config, ivy=interface)

	def show_shape_on_gcs(buffer_coords, id, color):
		msg_shape = PprzMessage("ground", "SHAPE")
		msg_shape['id'] = id
		msg_shape['linecolor'] = colo
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

	show_shape_on_gcs(buffer, id, color)



if __name__ == '__main__':
	main()