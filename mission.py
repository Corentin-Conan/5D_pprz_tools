#!/usr/bin/python3



class Mission(object):

	def __init__(self, name, airframe_url, flight_plan_url, description = None):
		self.name = name
		self.description = description
		self.airframe_file = airframe_file
		self.flight_plan_file = flight_plan_file