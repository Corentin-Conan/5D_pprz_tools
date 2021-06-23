#!/usr/bin/python3

from .5D_objects.task_order import TaskOrder
from .5D_objects.mission import Mission

class Controler(object):

	def __init__(self):

		self.pending_task_orders = []

		self.accepted_task_order = []

		self.pending_missions = []

		self.accepted_missions = []