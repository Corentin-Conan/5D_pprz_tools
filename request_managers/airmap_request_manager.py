#!/usr/bin/python3

import sys
from os import path, getenv

from .user_profile.airmap_profile import AirmapUserProfile
from .airmap_flight_plan.airmap_flight_plan import AirmapFlightPlan

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/5D_API/toolkit")

from flight_plan_tools import pprz_flight_plan_to_geojson
from flight_plan_tools import to_deg

import requests
import json
import threading
import time

class AirmapRequestManager(object):

	def __init__(self):
		super().__init__()
		self.airmap_user_profile = AirmapUserProfile()
		self.airmap_flight_plan = AirmapFlightPlan()
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
			url = "https://auth.airmap.com/realms/airmap/protocol/openid-connect/token"
			payload = {
				'grant_type': 'refresh_token',
				'client_id': self.airmap_user_profile.client_id,
				'refresh_token': self.airmap_user_profile.refresh_token
			}
			resp = requests.post(url, data=payload)
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
		airspaces = []
		params = (
			('geometry', json.dumps(geojson)),
			('types', 'airport,controlled_airspace'),
			('full', 'true'),
			('geometry_format', 'geojson')
		)
		response = requests.get('https://api.airmap.com/airspace/v2/search', headers=self.headers, params=params)
		print(response.text)
		airspaces = response.json()["data"]
		return airspaces

	def get_user_information(self):
		if self.airmap_user_profile.token is None:
			print("User not logged in")
			return
		self.airmap_user_profile.pilot_id = requests.get('https://api.airmap.com/pilot/v2/profile', headers=self.headers).json()["data"]["id"]
		print("Pilot id : " + self.airmap_user_profile.pilot_id)
		self.airmap_user_profile.aircraft_list = requests.get("https://api.airmap.com/pilot/v2/"+ self.airmap_user_profile.pilot_id +  "/aircraft", headers=self.headers).json()['data']
		print("Aircraft list : ")
		for aircraft in self.airmap_user_profile.aircraft_list:
			print(str(aircraft))

	def initiate_flight_plan(self, flight_plan_geometry, lat0, lon0):
		if self.airmap_user_profile.token is None:
			print("\nUser not logged in")
			return
		self.airmap_flight_plan.update_values(
			pilot_id = self.airmap_user_profile.pilot_id,
			ac_id = self.airmap_user_profile.aircraft_list[0]["id"],
			take_off_lon = to_deg(lon0),
			take_off_lat = to_deg(lat0),
			geometry = flight_plan_geometry)

	def create_flight_plan(self):
		payload = self.airmap_flight_plan.get_payload()
		url = "https://api.airmap.com/flight/v2/plan"
		response = requests.request("POST", url, json=payload, headers=self.headers)
		print("\nFlight plan being created")
		if response.status_code == 200:
			print("Flight plan created successfully")
			self.airmap_flight_plan.fp_id = response.json()['data']['id']
			print("Flight plan ID : " + self.airmap_flight_plan.fp_id)
		else:
			print("Issue in flight plan creation")
			print(response.text)

	def submit_flight_plan(self):
		if self.airmap_flight_plan.fp_id is None:
			print("No flight plan created, can't send one to Airmap")
			return
		print("Sending flight plan to Airmap")
		url = "https://api.airmap.com/flight/v2/plan/" + self.airmap_flight_plan.fp_id + "/submit"
		response = requests.request("POST", url, headers=self.headers)
		if response.status_code == 200:
			print("Flight plan successfully submited")
			self.airmap_flight_plan.flight_id = response.json()["data"]["flight_id"]
			print("Flight ID : " + str(self.airmap_flight_plan.flight_id))
		else:
			print("Issue in flight plan submission")
			print(response.text)

	def populate_flight_plan_confirmation_window(self, window):
		window.set_fields_from_dict(vars(self.airmap_flight_plan))

	def update_flight_plan_from_confirmation_window(self, window):
		dic = window.get_values()
		for elem in dic:
			if dic[elem] is not None:
				if elem == "fp_id":
					self.airmap_flight_plan.fp_id = dic[elem]
				if elem == "flight_id" :
					self.airmap_flight_plan.flight_id = dic[elem]
				if elem == "pilot_id":
					self.airmap_flight_plan.pilot_id = dic[elem]
				if elem == "ac_id":
					self.airmap_flight_plan.ac_id = dic[elem]
				if elem == "take_off_lon":
					self.airmap_flight_plan.take_off_lon = dic[elem]
				if elem == "take_off_lat":
					self.airmap_flight_plan.take_off_lat = dic[elem]
				if elem == "min_alt":
					self.airmap_flight_plan.min_alt = dic[elem]
				if elem == "max_alt":
					self.airmap_flight_plan.max_alt = dic[elem]
				if elem == "buf":
					self.airmap_flight_plan.buf = dic[elem]
				if elem == "start_time":
					self.airmap_flight_plan.start_time = dic[elem]
				if elem == "end_time":
					self.airmap_flight_plan.end_time = dic[elem]
				if elem == "flight_descr":
					self.airmap_flight_plan.flight_descr = dic[elem]
				if elem == "geometry":
					pass

	def show_fp_geometry_on_window(self, window, wps):
		x = []
		y = []
		points = self.airmap_flight_plan.geometry["coordinates"][0]
		for point in points:
			x.append(point[0])
			y.append(point[1])
		wpx = []
		wpy = []
		for wp in wps:
			wpx.append(wp.lon)
			wpy.append(wp.lat)
		window.plot(x, y)
		window.plot_points(wpx, wpy)
