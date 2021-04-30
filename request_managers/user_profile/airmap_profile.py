#!/usr/bin/python3

import json

class AirmapUserProfile(object):

	def __init__(self):
		super().__init__()
		with open('airmap.config.json') as f:
			data_user = json.load(f)
		self.api_key = data_user["airmap"]["api_key"]
		self.client_id = data_user["airmap"]["client_id"]
		self.password = data_user["airmap"]["password"]
		self.token = None
