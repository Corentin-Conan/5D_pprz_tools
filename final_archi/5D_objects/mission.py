#!/usr/bin/python3

class Mission(object):

	def __init__(self):
		super().__init__()
		self.date = None
		self.time = None
		self.activity = None
		self.location = None
		self.service = None
		self.pilot = None
		self.drone = None
		self.description = None


	def create_from_taks_order(self, task_order):
		return