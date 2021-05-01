#!/usr/bin/python3

import sys
from os import path, getenv

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan

class PprzRequestManager(object):

	def __init__(self):
		super().__init__()
		self.flight_plan = None

	def update_config(self, config):
		print("update config")
		self.flight_plan = FlightPlan.parse(config.flight_plan)
		for block in self.flight_plan.blocks:
			print(block.name)
			print(block.no)
			print(block.xml)
