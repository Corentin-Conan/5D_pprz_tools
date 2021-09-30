#!/usr/bin/python3

class TaskOrder(object):

	def __init__(self, activity = None, location = None, service = None, target = None, date = None, time = None, comment = None):
		super().__init__()

		# activity : AIRPORT INSPECTION / NAVAID INSPECTION / WATERDROME INSPECTION
		self.activity = activity
		# location : RHODES / CORFU / HEATHROW
		self.location = location
		# services for AIRPORT INSPECTION : TAXIWAY APRON INSPECTION / TAXIWAY LIGHT INSPECTION / FOD DETECTION / PERIMETER SURVEILLANCE / INFRASTRUCTURE INSPECTION
		# services for NAVAID INSPECTION : VOR EXTENDED GROUND TEST / VOR SHORT RANGE FLIGHT TEST / DME DME INSPECTION
		# services for WATERDROME INSPECTION : WATERWAY INSPECTION / INFRASTRUCTURE INSPECTION
		self.service = service
		# target for AIRPORT INSPECTION : AIRFIELD SECTION #XX / RUNWAY #XX / BUILDING #XX / PERIMETER SECTION #XX
		# target for NAVAID INSPECTION : VOR #XX / DME-DME #XX
		# target for WATERDROME INSPECTION : WATERWAY #XX / FACILITY SECTION #XX
		self.target = target
		# date format: yyyy-MM-dd
		# TODO func to format date if at an other format
		self.date = date
		# time format: HH:mm:ss
		# TODO func to format time if at an other format
		self.time = time
		#
		self.comment = comment


		self.status = "PENDING"

	