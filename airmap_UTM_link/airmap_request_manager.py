#!/usr/bin/python3

import requests
import json
import threading
import time
from pathlib import Path
from geojson import Polygon
from geojson_rewind import rewind

from flight_plan_widget import FlightPlanWidget
from airspace_list_widgets import AirspaceWidget, AirspaceTypeWidget



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
		self.aircrafts = []

		self.flight_plan = None

		self.airspace_type_widgets = []
		self.airspace_widgets = []


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

		url = "https://api.airmap.com/pilot/v2/" + self.pilot_id + "/aircraft"
		response = requests.get(url, headers = self.headers)
		self.aircrafts = response.json()["data"]
		print("Aircrafts : " + str(self.aircrafts))


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

		# create geojson object
		mission_airspace = Polygon([[[i,j] for i,j in geometry]])

		# rewind coordinates (put them in order according to right hand rule)
		mission_airspace_rewound = rewind(mission_airspace)

		payload = {
			"pilot_id": self.pilot_id,
			"aircraft_id": self.aircrafts[0]["id"],
			"start_time": start_time,
			"end_time": end_time,
			"takeoff_latitude": takeoff_latitude,
			"takeoff_longitude": takeoff_longitude,
			"min_altitude_agl": min_altitude_agl,
			"max_altitude_agl": max_altitude_agl,
			"buffer": buffer,
			"geometry": mission_airspace_rewound,
			"flight_description": flight_description
		}

		# create flight plan
		url = "https://api.airmap.com/flight/v2/plan"
		response = requests.post(url, json = payload, headers = self.headers)
		print(response.text)

		self.flight_plan = response.json()["data"]

		# submit flight plan
		url = "https://api.airmap.com/flight/v2/plan/" + self.flight_plan["id"] + "/submit"
		response = requests.post(url, headers = self.headers)
		print(response.text)

		if response.status_code == 200:

			return response.json()["data"]["flight_id"]


	# get airspaces near pprz flight plan geometry
	def get_airspaces_in_geometry(self, geometry):

		querystring = (
			('geometry', geometry),
			('full', 'true'),
			('geometry_format', 'geojson')
		)

		response = requests.get('https://api.airmap.com/airspace/v2/search', headers = self.headers, params = querystring)
		print(response.text)

		if response.status_code == 200:

			airspaces = response.json()['data']
			print(airspaces)

			# reset list of airspace type widgets
			self.airspace_type_widgets = []

			# create airspace type widgets and their children airspace widget
			airspace_id = 10

			for airspace in airspaces:

				airspace_id += 1

				airspace_widget = AirspaceWidget(airspace_id, airspace)

				type = airspace_widget.type

				if type not in [airspace_type_widget.type for airspace_type_widget in self.airspace_type_widgets]:

					airspace_type_widget = AirspaceTypeWidget(type, airspace_widget)
					self.airspace_type_widgets.append(airspace_type_widget)

				else:

					airspace_type_widget = next(x for x in self.airspace_type_widgets if x.type == type)
					airspace_type_widget.add_child(airspace_widget)

			return self.airspace_type_widgets



