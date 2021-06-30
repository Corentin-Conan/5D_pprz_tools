#!/usr/bin/python3

class Mission(object):

	def __init__(self, date = None, time = None, activity = None, location = None, service = None, target = None, dmo = None, dso = None, drone = None, description = None):
		super().__init__()
		self.date = date
		# date format: yyyy-MM-dd
		# TODO func to format date if at an other format
		self.time = time
		# time format: HH:mm:ss
		# TODO func to format time if at an other format
		self.activity = activity
		# activity : AIRPORT INSPECTION / NAVAID INSPECTION / WATERDROME INSPECTION
		self.location = location 
		# location : RHODES / CORFU / HEATHROW
		self.service = service
		# services for AIRPORT INSPECTION : TAXIWAY APRON INSPECTION / TAXIWAY LIGHT INSPECTION / FOD DETECTION / PERIMETER SURVEILLANCE / INFRASTRUCTURE INSPECTION
		# services for NAVAID INSPECTION : VOR EXTENDED GROUND TEST / VOR SHORT RANGE FLIGHT TEST / DME DME INSPECTION
		# services for WATERDROME INSPECTION : WATERWAY INSPECTION / INFRASTRUCTURE INSPECTION
		self.target = target
		# target for AIRPORT INSPECTION : AIRFIELD SECTION #XX / RUNWAY #XX / BUILDING #XX / PERIMETER SECTION #XX
		# target for NAVAID INSPECTION : VOR #XX / DME-DME #XX
		# target for WATERDROME INSPECTION : WATERWAY #XX / FACILITY SECTION #XX
		self.dmo = dmo
		#
		self.dso = dso
		#
		self.drone = drone
		#
		self.description = description
		#


	def create_from_taks_order(self, task_order):
		return
