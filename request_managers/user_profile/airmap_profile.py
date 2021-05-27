#!/usr/bin/python3

import json
from pathlib import Path

class AirmapUserProfile(object):

	def __init__(self):
		super().__init__()
		with open(Path(__file__).parent / 'airmap.config.json') as f:
			data_user = json.load(f)
		self.api_key = data_user["airmap"]["api_key"]
		self.client_id = data_user["airmap"]["client_id"]
		self.password = data_user["airmap"]["password"]
		self.user_name = data_user["airmap"]["user_name"]
		self.token = None
		self.refresh_token = None
		self.pilot_id = None
		self.aircraft_list = None