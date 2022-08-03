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


def trial1_2_1_nominal_init():

	interface = IvyMessagesInterface("msgInterface")
	pprzconnect = PprzConnect(notify=update_config, ivy=interface)
	
	# WW4
	msg_shape = PprzMessage("ground", "SHAPE")
	msg_shape['id'] = 3
	msg_shape['linecolor'] = "red"
	msg_shape['fillcolor'] = "red"
	msg_shape['opacity'] = 1
	msg_shape['shape'] = 1
	msg_shape['status'] = 0 
	lonarr = [39.635409, 39.640293]
	latarr = [19.894519, 19.902712]
	for i in range(len(lonarr)):
		lonarr[i] *= 10000000
		lonarr[i] = int(lonarr[i])
	for i in range(len(latarr)):
		latarr[i] *= 10000000
		latarr[i] = int(latarr[i])
	msg_shape['latarr'] = lonarr
	msg_shape['lonarr'] = latarr
	msg_shape['text'] = "WW4"
	print(msg_shape)
	interface.send(msg_shape)

	# WW2
	msg_shape = PprzMessage("ground", "SHAPE")
	msg_shape['id'] = 4
	msg_shape['linecolor'] = "red"
	msg_shape['fillcolor'] = "red"
	msg_shape['opacity'] = 1
	msg_shape['shape'] = 1
	msg_shape['status'] = 0 
	lonarr = [39.636297, 39.633049]
	latarr = [19.908478, 19.916611]
	for i in range(len(lonarr)):
		lonarr[i] *= 10000000
		lonarr[i] = int(lonarr[i])
	for i in range(len(latarr)):
		latarr[i] *= 10000000
		latarr[i] = int(latarr[i])
	msg_shape['latarr'] = lonarr
	msg_shape['lonarr'] = latarr
	msg_shape['text'] = "WW2"
	print(msg_shape)
	interface.send(msg_shape)

	# WW1
	msg_shape = PprzMessage("ground", "SHAPE")
	msg_shape['id'] = 5
	msg_shape['linecolor'] = "red"
	msg_shape['fillcolor'] = "red"
	msg_shape['opacity'] = 1
	msg_shape['shape'] = 1
	msg_shape['status'] = 0 
	lonarr = [39.632067, 39.633446]
	latarr = [19.915336, 19.924045]
	for i in range(len(lonarr)):
		lonarr[i] *= 10000000
		lonarr[i] = int(lonarr[i])
	for i in range(len(latarr)):
		latarr[i] *= 10000000
		latarr[i] = int(latarr[i])
	msg_shape['latarr'] = lonarr
	msg_shape['lonarr'] = latarr
	msg_shape['text'] = "WW1"
	print(msg_shape)
	interface.send(msg_shape)

	# WW3
	msg_shape = PprzMessage("ground", "SHAPE")
	msg_shape['id'] = 6
	msg_shape['linecolor'] = "red"
	msg_shape['fillcolor'] = "red"
	msg_shape['opacity'] = 1
	msg_shape['shape'] = 1
	msg_shape['status'] = 0 
	lonarr = [39.636414, 39.638751]
	latarr = [19.924865, 19.916064]
	for i in range(len(lonarr)):
		lonarr[i] *= 10000000
		lonarr[i] = int(lonarr[i])
	for i in range(len(latarr)):
		latarr[i] *= 10000000
		latarr[i] = int(latarr[i])
	msg_shape['latarr'] = lonarr
	msg_shape['lonarr'] = latarr
	msg_shape['text'] = "WW3"
	print(msg_shape)
	interface.send(msg_shape)


def main():
	trial1_2_1_nominal_init()

if __name__ == '__main__':
	main()