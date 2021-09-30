#!/usr/bin/python3

import json
from pathlib import Path

class FINTUserProfile(object):

	def __init__(self):
		super().__init__()
		with open(Path(__file__).parent / 'fint.config.json') as f:
			data_user = json.load(f)
		self.password = data_user["fint"]["password"]
		self.user_name = data_user["fint"]["username"]
		self.token = None
		self.refresh_token = None