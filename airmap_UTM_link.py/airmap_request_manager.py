#!/usr/bin/python3

import requests
import json
import threading
import time
from pathlib import Path

from flight_plan_widget import FlightPlanWidget



class AirmapRequestManager():


	def __init__(self):

		with open(Path(__file__).parent / 'airmap.config.json') as f:
			data_user = json.load(f)

		self.api_key = data_user["airmap"]["api_key"]
		self.client_id = data_user["airmap"]["client_id"]
		self.user_name = "corentin.conan@enac.fr"
		self.password = "Pprz_2021"

		self.token = None
		self.refresh_token = None

		self.headers = None

		self.pilot_id = None


	def log_in_to_airmap_API(self, client_id, user_name, password, connection_status_label):
		
		print("\nLogging in ...")

		user_payload = {
			'grant_type': 'password',
			'client_id': client_id,
			'username': user_name,
			'password': password
		}

		auth_response = requests.post(
			"https://auth.airmap.com/realms/airmap/protocol/openid-connect/token", 
			data = user_payload)

		if auth_response.status_code == 200:

			print(auth_response.text)
			connection_status_label.setStyleSheet("color: rgb(50,200,50)")
			connection_status_label.setText("Connected")

			self.token = auth_response.json()["access_token"]
			self.refresh_token = auth_response.json()["refresh_token"]

			self.headers = {
				"Accept": "application/json",
				"Content-Type": "application/json; charset=utf-8",
				"Authorization": "Bearer " + self.token,
		    	"X-API-KEY": self.api_key
			}

			print("User logged in to Airmap API")

			refresh_thread = threading.Thread(target = self.thread_refresh, 
				args = (auth_response.json()["expires_in"] - 100, connection_status_label,), 
				daemon = True)

			refresh_thread.start()
			self.get_user_profile()

		else :

			print("User not logged in " + str(auth_response.text))


	## thread meant to refresh the airmap access token
	def thread_refresh(self, refresh_timer, connection_status_label = None):
		
		while(True):

			print("\nStarting token refresh thread")
			time.sleep(refresh_timer)
			print("\nAutomatic Airmap token refresh ...")

			connection_status_label.setStyleSheet("color: rgb(150,150,150)")
			connection_status_label.setText("Refreshing Token")

			url = "https://auth.airmap.com/realms/airmap/protocol/openid-connect/token"
			payload = {
				'grant_type': 'refresh_token',
				'client_id': self.client_id,
				'refresh_token': self.refresh_token
			}
			resp = requests.post(url, data=payload)

			if resp.status_code == 200:

				print("Automatic token refresh success")
				self.refresh_token = resp.json()["refresh_token"]
				self.token = resp.json()["refresh_token"]
				
				if connection_status_label is not None:

					connection_status_label.setStyleSheet("color: rgb(50,200,50)")
					connection_status_label.setText("Connected")
			
			else:

				print("Failing to refresh token ; status code = " + str(resp.status_code))
				
				if connection_status_label is not None:

					connection_status_label.setStyleSheet("color: rgb(255,0,0)")
					connection_status_label.setText("Refresh Token Failed")


	def get_user_profile(self):

		print("\nRetreiving user information ...")
		response = requests.get("https://api.airmap.com/pilot/v2/profile", headers = self.headers)
		print("User logged in")
		print(response.text)
		self.pilot_id = response.json()["data"]["id"]


	def load_flight_plans(self):

		print("\nLoading flights ...")
		querystring = {"pilot_id": self.pilot_id}
		response = requests.get("https://api.airmap.com/flight/v2/", headers = self.headers, params = querystring)
		print(response.text)

		flights = response.json()["data"]["results"]
		flight_widgets = []

		for flight in flights:

			flight_widget = FlightPlanWidget(flight)
			flight_widgets.append(flight_widget)

		return flight_widgets


	def delete_flight(self, flight_id):

		url = "https://api.airmap.com/flight/v2/" + flight_id + "/delete"
		response = requests.post(url, headers = self.headers)

		print(response.text)


	def create_flight_plan(self, pilot_id, aircraft_id, start_time, end_time,
		takeoff_latitude, takeoff_longitude, min_altitude_agl, max_altitude_agl,
		buffer, geometry, flight_description):

		payload = {
			"pilot_id": pilot_id,
			"aircraft_id": aircraft_id,
			"start_time": start_time,
			"end_time": end_time,
			"takeoff_latitude": takeoff_latitude,
			"takeoff_longitude": takeoff_longitude,
			"min_altitude_agl": min_altitude_agl,
			"max_altitude_agl": max_altitude_agl,
			"buffer": buffer,
			"geometry": geometry,
			"flight_description": flight_description
		}

		url = "https://api.airmap.com/flight/v2/plan"

		response = requests.post(url, json = payload, headers = self.headers)
		print(response.text)


