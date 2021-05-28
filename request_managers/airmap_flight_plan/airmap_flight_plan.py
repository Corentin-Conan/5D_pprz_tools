#!/usr/bin/python3

import requests
import json

class AirmapFlightPlan(object):

	def __init__(self, fp_id = None, flight_id = None, pilot_id = None, ac_id = None, 
		take_off_lon = None, take_off_lat = None, min_alt = None, max_alt = None, buf = None,
		start_time = None, end_time = None, flight_descr = None, geometry = None):
		super().__init__()
		self.fp_id = fp_id
		self.flight_id = flight_id
		self.pilot_id = pilot_id
		self.ac_id = ac_id
		self.take_off_lon = take_off_lon
		self.take_off_lat = take_off_lat
		self.min_alt = min_alt
		self.max_alt = max_alt
		self.buf = buf
		self.start_time = start_time
		self.end_time = end_time
		self.flight_descr = flight_descr
		self.geometry = geometry
		self.has_been_sent = False
		self.has_been_submitted = False

	def get_payload(self):
		payload = {
		    "pilot_id": self.pilot_id,
		    "aircraft_id": self.ac_id,
		    "start_time": self.start_time,
		    "end_time": self.end_time,
		    "takeoff_latitude": self.take_off_lat,
		    "takeoff_longitude": self.take_off_lon,
		    "min_altitude_agl": self.min_alt,
		    "max_altitude_agl": self.max_alt,
		    "buffer": self.buf,
		    "geometry": self.geometry
		}
		if any(elem is None for elem in payload.values()):
			print("Not enough information to generate payload")
			print("Payload : " + str(payload))
			return
		return payload

	def update_values(self, fp_id = None, flight_id = None, pilot_id = None, ac_id = None, 
		take_off_lon = None, take_off_lat = None, min_alt = None, max_alt = None, buf = None,
		start_time = None, end_time = None, flight_descr = None, geometry = None):
		if fp_id is not None:
			self.fp_id = fp_id
		if flight_id is not None:
			self.flight_id = flight_id
		if pilot_id is not None:
			self.pilot_id = pilot_id
		if ac_id is not None:
			self.ac_id = ac_id
		if take_off_lon is not None:
			self.take_off_lon = take_off_lon
		if take_off_lat is not None:
			self.take_off_lat = take_off_lat
		if min_alt is not None:
			self.min_alt = min_alt
		if max_alt is not None:
			self.max_alt = max_alt
		if buf is not None:
			self.buf = buf
		if start_time is not None:
			self.start_time = start_time
		if end_time is not None:
			self.end_time = end_time
		if flight_descr is not None:
			self.flight_descr = flight_descr
		if geometry is not None:
			self.geometry = geometry
