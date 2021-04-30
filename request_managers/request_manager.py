#!/usr/bin/python3

from .airmap_request_manager import AirmapRequestManager
from .fint_request_manager import FintRequestManager
from .pprz_request_manager import PprzRequestManager

## This is the main request manager
## This program is in direct link with the UI
## It uses functions from sub request managers

class RequestManager(object):

	def __init__(self):
		super().__init__()
		## sub request managers instanciation 
		self.airmap_request_manager = AirmapRequestManager()
		self.fint_request_manager = FintRequestManager()
		self.pprz_request_manager = PprzRequestManager()

