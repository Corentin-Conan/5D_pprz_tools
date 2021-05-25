#!/usr/bin/python3

import sys
from os import path, getenv

from .user_profile.airmap_profile import AirmapUserProfile

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/5D_API/toolkit")

from flight_plan_tools import pprz_flight_plan_to_geojson

import requests
import json
import threading
import time

class AirmapRequestManager(object):

	def __init__(self):
		super().__init__()
		self.airmap_user_profile = AirmapUserProfile()
		self.headers = None

	def update_credentials(self, client_id, user_name, password):
		self.airmap_user_profile.client_id = client_id
		self.airmap_user_profile.user_name = user_name
		self.airmap_user_profile.password = password

	def log_in(self, connection_status_label):
		print("\nLogging in ...")
		user_payload = {
			'grant_type': 'password',
			'client_id': self.airmap_user_profile.client_id,
			'username': self.airmap_user_profile.user_name,
			'password': self.airmap_user_profile.password
		}
		self.auth_response = requests.post(
			"https://auth.airmap.com/realms/airmap/protocol/openid-connect/token", 
			data = user_payload)
		if self.auth_response.status_code == 200:
			self.airmap_user_profile.token = self.auth_response.json()["access_token"]
			self.airmap_user_profile.refresh_token = self.auth_response.json()["refresh_token"]
			self.headers = {
		    	"Accept": "application/json",
		    	"Content-Type": "application/json; charset=utf-8",
		    	"Authorization": "Bearer " + self.airmap_user_profile.token,
		    	"X-API-KEY": self.airmap_user_profile.api_key
			}
			print("User logged in to Airmap API")
			connection_status_label.setStyleSheet("color: rgb(50,200,50)")
			connection_status_label.setText("Connected")
			refresh_thread = threading.Thread(target = self.thread_refresh, 
				args = (self.auth_response.json()["expires_in"] - 100, connection_status_label,), 
				daemon = True)
			refresh_thread.start()
		else :
			print("User not logged in " + str(self.auth_response.text))
			connection_status_label.setStyleSheet("color: rgb(255,0,0)")
			connection_status_label.setText("Not Connected")

	def thread_refresh(self, refresh_timer, connection_status_label):
		## thread meant to refresh the airmap access token
		while(True):
			time.sleep(refresh_timer)
			print("\nAutomatic Airmap token refresh ...")
			connection_status_label.setStyleSheet("color: rgb(150,150,150)")
			connection_status_label.setText("Refreshing Token")
			URL = "https://auth.airmap.com/realms/airmap/protocol/openid-connect/token"
			PAYLOAD = {
				'grant_type': 'refresh_token',
				'client_id': self.airmap_user_profile.client_id,
				'refresh_token': self.airmap_user_profile.refresh_token
			}
			resp = requests.post(URL, data=PAYLOAD)
			if resp.status_code == 200:
				print("Automatic token refresh success")
				self.airmap_user_profile.refresh_token = resp.json()["refresh_token"]
				self.airmap_user_profile.token = resp.json()["refresh_token"]
				connection_status_label.setStyleSheet("color: rgb(50,200,50)")
				connection_status_label.setText("Connected")
			else:
				print("Failing to refresh token ; status code = " + str(resp.status_code))
				connection_status_label.setStyleSheet("color: rgb(255,0,0)")
				connection_status_label.setText("Refresh Token Failed")

	def get_airspaces_in_geometry(self, geojson):
		if self.airmap_user_profile.token is None:
			print("User not logged in")
			return
		if geojson is None:
			print("\nNo GeoJson flight plan defined")
			return 
		airspaces = []
		params = (
			('geometry', json.dumps(geojson)),
			('types', 'airport,controlled_airspace'),
			('full', 'true'),
			('geometry_format', 'geojson')
		)
		response = requests.get('https://api.airmap.com/airspace/v2/search', headers=self.headers, params=params)
		# print(response.text)
		airspaces = response.json()["data"]
		return airspaces


	def submit_flight_plan(self, flight_plan):
		print("Submit flight plan function not yet implemented")
		return 0
