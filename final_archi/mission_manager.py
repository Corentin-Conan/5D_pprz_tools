#!/usr/bin/python3

from datetime import datetime

from objects.task_order import TaskOrder
from objects.mission import Mission



class MissionManager(object):

	def __init__(self):

		self.pending_task_orders = {"HEATHROW" : [], "RHODES" : [], "CORFU" : []}

		self.accepted_task_orders = {"HEATHROW" : [], "RHODES" : [], "CORFU" : []}

		self.pending_missions = {"HEATHROW" : [], "RHODES" : [], "CORFU" : []}

		self.accepted_missions = {"HEATHROW" : [], "RHODES" : [], "CORFU" : []}
		# current date and time to create the missions at a realistic date
		dateTime = datetime.now()

		# fake missions for the sake of the demonstration
		self.mission1 = Mission(
			date = "{}-{}-{}".format(dateTime.year, dateTime.month, dateTime.day + 1),
			time = "14:30:00",
			activity = "AIRPORT INSPECTION",
			location = "HEATHROW",
			service = "TAXIWAY APRON INSPECTION",
			target = "AIRFIELD SECTION #13",
			dmo = "John Doe",
			dso = "Jack Doe",
			description = "Regular inspection of the section 13 of the airfiel.")
		self.mission2 = Mission(
			date = "{}-{}-{}".format(dateTime.year, dateTime.month, dateTime.day + 2),
			time = "08:00:00",
			activity = "AIRPORT INSPECTION",
			location = "HEATHROW",
			service = "INFRASTRUCTURE INSPECTION",
			target = "BUILDING #2",
			dmo = "John Doe",
			dso = "Jack Doe",
			description = "Inspection of terminal 2 roof for engineering reasons.")
		self.accepted_missions["HEATHROW"].append(self.mission1)
		self.accepted_missions["HEATHROW"].append(self.mission2)

		self.mission3 = Mission(
			date = "{}-{}-{}".format(dateTime.year, dateTime.month, dateTime.day + 1),
			time = "16:00:00",
			activity = "NAVAID INSPECTION",
			location = "RHODES",
			service = "VOR EXTENDED GROUND TEST",
			target = "VOR #2",
			dmo = "John Doe",
			dso = "Jack Doe",
			description = "VOR number 2 signal inspection.")
		self.mission4 = Mission(
			date = "{}-{}-{}".format(dateTime.year, dateTime.month, dateTime.day + 2),
			time = "07:00:00",
			activity = "NAVAID INSPECTION",
			location = "RHODES",
			service = "VOR SHORT RANGE FLIGHT TEST",
			target = "VOR #1",
			dmo = "John Doe",
			dso = "Jack Doe",
			description = "VOR number 1 short range flight test.")
		self.accepted_missions["RHODES"].append(self.mission3)
		self.accepted_missions["RHODES"].append(self.mission4)

		self.mission5 = Mission(
			date = "{}-{}-{}".format(dateTime.year, dateTime.month, dateTime.day + 1),
			time = "9:35:00",
			activity = "WATERDROME INSPECTION",
			location = "CORFU",
			service = "WATERWAY INSPECTION",
			target = "WATERWAY #2",
			dmo = "John Doe",
			dso = "Jack Doe",
			description = "Inspection of waterway number 2 15min before landing of seaplane.")
		self.mission6 = Mission(
			date = "{}-{}-{}".format(dateTime.year, dateTime.month, dateTime.day + 1),
			time = "10:10:00",
			activity = "WATERDROME INSPECTION",
			location = "CORFU",
			service = "WATERWAY INSPECTION",
			target = "WATERWAY #2",
			dmo = "John Doe",
			dso = "Jack Doe",
			description = "Inspection of waterway number 2 15min before landing of seaplane.")
		self.accepted_missions["CORFU"].append(self.mission5)
		self.accepted_missions["CORFU"].append(self.mission6)
