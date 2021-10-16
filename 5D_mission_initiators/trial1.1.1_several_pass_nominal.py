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

def update_config(conf):
	pass


def trial1_1_1_init():

	interface = IvyMessagesInterface("msgInterface")
	pprzconnect = PprzConnect(notify=update_config, ivy=interface)
	
	# show area to inspect on map
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
	trial1_1_1_init()

if __name__ == '__main__':
	main()