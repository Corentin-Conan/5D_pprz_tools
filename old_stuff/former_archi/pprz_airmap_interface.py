#!/usr/bin/python3

import requests
import tools as myTools
import sys
from os import path, getenv
import json

# import telemetry_interface as tl

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan

class Pprz_UTM_Interface(object):

	def __init__(self, ivy_interface):
		## variables
		self.flight_plan = None
		self.airspace_list = None

		## connection to pprz
		self._interface = ivy_interface
		self.pprzconnect = PprzConnect(notify=self.update_config, ivy=self._interface)

		## connection to Airmap API
		self.CLIENT_ID = "2cd97349-096e-4457-be5d-bd1e751380ef"
		self.USER_NAME = "corentin.conan@enac.fr"
		self.PASSWORD = "Pprz_2021"
		self.API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHxvd2FENUdZQzNLV3YwQkN3b1h2ZDh1bkRlenAzIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnxhZExxdm4zU05QcG5CWmlHTTlvb0x0RVgzTG5XIiwib3JnYW5pemF0aW9uX2lkIjoiZGV2ZWxvcGVyfFAzS0xHWUVjTmtPTERERkwzRGxHcWh5Z2VSMFgiLCJpYXQiOjE2MTY1MDQ5NjF9.CknSj6XPvJCVwc4WhzqATdeOZcOVMxSt03FIqW_KDG4"
		self.TOKEN = None
		self.PILOT_ID = None
		self.AIRCRAFT_IDs = []
		self.FLIGHT_PLAN_ID = None
		self.PAYLOAD = {
			'grant_type': 'password',
			'client_id': self.CLIENT_ID,
			'username': self.USER_NAME,
			'password': self.PASSWORD
		}
		self.auth_response = None
		self.TOKEN = None
		self.headers = None
		## get pilot ID
		self.PILOT_ID = None
		## get aircrafts ID
		self.all_aircrafts = None
		self.own_flight_ids = []
		## store flight plan geometry
		self.flight_plan_geometry = None
		## store flights in in flight plan geometry
		self.flights_in_flight_plan_geometry = None
		## telemetry interface
		# self.telemetry_interface = tl.TelemetryInterface(self._interface)
		## flight key
		self.flight_key = None

	def stop(self):
		if self._interface is not None:
			self._interface.shutdown()

	def __del__(self):
		self.stop()

	def log_in(self, client_id, username, password):
		user_payload = {
			'grant_type': 'password',
			'client_id': client_id,
			'username': username,
			'password': password
		}
		self.auth_response = requests.post(
			"https://auth.airmap.com/realms/airmap/protocol/openid-connect/token", 
			data = user_payload)
		if self.auth_response.status_code == 200:
			self.TOKEN = self.auth_response.json()["access_token"]
			print("User logged in hhhhh")
			self.headers = {
		    	"Accept": "application/json",
		    	"Content-Type": "application/json; charset=utf-8",
		    	"Authorization": "Bearer " + self.TOKEN,
		    	"X-API-KEY": self.API_KEY
			}
			self.get_user_information()
			return(1)
		else :
			print("User not logged in " + str(self.auth_response.text))
			return(0)

	def print_connexion_details(self):
		if self.TOKEN is not None:
			print(self.auth_response.text)
		else:
			print("User not logged in ")

	def get_user_information(self):
		if self.TOKEN is not None:
			#get pilot ID
			response = requests.get('https://api.airmap.com/pilot/v2/profile', headers=self.headers)
			# self.PILOT_ID = requests.get('https://api.airmap.com/pilot/v2/profile', headers=self.headers).json()["data"]["id"]
			print(response.text)
			#get aircrafts ID
			self.all_aircrafts = requests.get("https://api.airmap.com/pilot/v2/"+ self.PILOT_ID +  "/aircraft", headers=self.headers).json()['data']
			for aircraft in self.all_aircrafts:
				self.AIRCRAFT_IDs.append(aircraft['id'])
		else:
			print("User not logged in")

	def update_config(self, config):
		self.flight_plan = FlightPlan.parse(config.flight_plan)

	def create_flight_plan(self):
		self.get_user_information()
		## get information from current flight plan
		max_dist = float(self.flight_plan.max_dist_from_home)
		lat0 = float(myTools.dms_to_deg(self.flight_plan.lat0))
		lon0 = float(myTools.dms_to_deg(self.flight_plan.lon0))
		## params to create flight plan
		url = "https://api.airmap.com/flight/v2/plan"
		mission_airspace = {"type":"Polygon","coordinates":[[[myTools.add_lon_and_meters(lon0, lat0, max_dist), myTools.sub_lat_and_meters(lat0, max_dist)],[myTools.add_lon_and_meters(lon0, lat0, max_dist),myTools.add_lat_and_meters(lat0, max_dist)],[myTools.sub_lon_and_meters(lon0, lat0, max_dist), myTools.add_lat_and_meters(lat0, max_dist)],[myTools.sub_lon_and_meters(lon0, lat0, max_dist), myTools.sub_lat_and_meters(lat0, max_dist)], [myTools.add_lon_and_meters(lon0, lat0, max_dist),myTools.sub_lat_and_meters(lat0, max_dist)]]]}
		# self.flight_plan_geometry = mission_airspace
		# mission_airspace = myTools.generate_geojson_from_xml(xml_file)
		payload = {
		    "pilot_id": self.PILOT_ID,
		    "aircraft_id": self.AIRCRAFT_IDs[0],
		    "start_time": "2021-10-01T13:39:52Z",
		    "end_time": "2022-10-01T16:39:52Z",
		    "takeoff_latitude": lat0,
		    "takeoff_longitude": lon0,
		    "min_altitude_agl": 18,
		    "max_altitude_agl": 73,
		    "buffer": 1,
		    "geometry": mission_airspace
		}
		response = requests.request("POST", url, json=payload, headers=self.headers)
		self.FLIGHT_PLAN_ID = response.json()['data']['id']
		print(response.text)


	def get_UTM_airspace(self):
		max_dist = float(self.flight_plan.max_dist_from_home)
		lat0 = float(myTools.dms_to_deg(self.flight_plan.lat0))
		lon0 = float(myTools.dms_to_deg(self.flight_plan.lon0))
		mission_airspace = {"type":"Polygon","coordinates":[[[myTools.add_lon_and_meters(lon0, lat0, max_dist), myTools.sub_lat_and_meters(lat0, max_dist)],[myTools.add_lon_and_meters(lon0, lat0, max_dist),myTools.add_lat_and_meters(lat0, max_dist)],[myTools.sub_lon_and_meters(lon0, lat0, max_dist), myTools.add_lat_and_meters(lat0, max_dist)],[myTools.sub_lon_and_meters(lon0, lat0, max_dist), myTools.sub_lat_and_meters(lat0, max_dist)], [myTools.add_lon_and_meters(lon0, lat0, max_dist),myTools.sub_lat_and_meters(lat0, max_dist)]]]}
		params = (
			('geometry', json.dumps(mission_airspace)),
			('types', 'airport,controlled_airspace'),
			('full', 'true'),
			('geometry_format', 'geojson')
		)
		response = requests.get('https://api.airmap.com/airspace/v2/search', headers=self.headers, params=params)
		# print(response)
		self.airspace_list = response.json()["data"]
		for airspace in self.airspace_list:
			print("\nID : " + airspace["id"])
			print("NAME : " + airspace["name"])
			print("PROPERTIES : " + str(airspace["properties"]))


	def submit_flight_plan(self):
		## submit flight plan to airmap API
		url = "https://api.airmap.com/flight/v2/plan/" + self.FLIGHT_PLAN_ID + "/submit"
		response = requests.request("POST", url, headers=self.headers)
		print(response.text)

	def add_aircraft(self, aircraft_model_id):
		data = '{"model_id":'+aircraft_model_id+',"nickname":"My drone"}'
		response = requests.post('https://api.airmap.com/pilot/v2/'+self.PILOT_ID+'/aircraft', headers=self.headers, data=data)
		print(response.text)

	def get_own_flights(self):
		querystring = {"pilot_id":self.PILOT_ID}
		response = requests.get("https://api.airmap.com/flight/v2/", headers=self.headers, params=querystring)
		for own_flight in response.json()['data']['results']:
			self.own_flight_ids.append(own_flight['id'])
		return(self.own_flight_ids)

	def get_flights_in_mission_airspace(self):
		max_dist = float(self.flight_plan.max_dist_from_home)
		lat0 = float(myTools.dms_to_deg(self.flight_plan.lat0))
		lon0 = float(myTools.dms_to_deg(self.flight_plan.lon0))
		mission_airspace = {"type":"Polygon","coordinates":[[[myTools.add_lon_and_meters(lon0, lat0, max_dist), myTools.sub_lat_and_meters(lat0, max_dist)],[myTools.add_lon_and_meters(lon0, lat0, max_dist),myTools.add_lat_and_meters(lat0, max_dist)],[myTools.sub_lon_and_meters(lon0, lat0, max_dist), myTools.add_lat_and_meters(lat0, max_dist)],[myTools.sub_lon_and_meters(lon0, lat0, max_dist), myTools.sub_lat_and_meters(lat0, max_dist)], [myTools.add_lon_and_meters(lon0, lat0, max_dist),myTools.sub_lat_and_meters(lat0, max_dist)]]]}
		querystring = {"geometry" : json.dumps(mission_airspace)}
		response = requests.get('https://api.airmap.com/flight/v2/', headers = self.headers, params = querystring)
		print(response.json()['data']['results'])

	def show_UTM_airspace(self):
		msg_list = myTools.pprzShapeMessage_from_GeoJSON(self.airspace_list)
		for msg in msg_list:
			self._interface.send(msg)

	def get_advisory_for_flight_plan(self):
		response = requests.get('https://api.airmap.com/advisory/v2/airspace/'+self.FLIGHT_PLAN_ID, headers=self.headers)
		print(response.json())

	def start_flight_comms(self):
		self.get_user_information()
		self.get_own_flights()
		## initiate telemetry interface
		response = requests.post('https://api.airmap.com/flight/v2/'+self.own_flight_ids[0]+'/start-comm', headers=self.headers)
		print(response.text)
		self.flight_key = response.json()['data']['key']
		print("Flight key : " + self.flight_key)
		# self.telemetry_interface.authentify(self.TOKEN, self.flight_key)
		# response = requests.post('https://api.airmap.com/flight/v2/'+self.own_flight_ids[0]+'/end-comm', headers=self.headers)
		# print(response.text)

	def print_telemetry(self):
		self._interface.subscribe(self.print_flight_params, PprzMessage("ground", "FLIGHT_PARAM"))

	def print_flight_params(self, msg_id, msg):
		print(str(msg))

	def send_telemetry(self):
		return 0

	# def test_telemtry(self):
	# 	data = {
	# 		'flight_id': self.own_flight_ids[1],
	# 		'rate': '1s',
	# 		'start': '2022-03-23T13:39:52Z',
	# 		'end': '2022-03-23T16:39:52Z'
	# 	}
	# 	print(self.headers)
	# 	print(data)
	# 	response = requests.get('https://api.airmap.com/archive/v1/telemetry/position', headers=self.headers, data=data)
	# 	print(response.text)

if __name__ == "__main__":
	pprz_UTM_interface = Pprz_UTM_Interface()
	if pprz_UTM_interface.flight_plan is not None:
		pprz_UTM_interface.get_UTM_airspace()
		pprz_UTM_interface.show_UTM_airspace()
		# pprz_UTM_interface.add_aircraft('"ba5ae61b-5c2e-4511-8b16-c49699ab2988"') # don't add too many aircrafts
		pprz_UTM_interface.create_flight_plan()
		pprz_UTM_interface.submit_flight_plan() # don't submit too many flight plans
		# print(pprz_UTM_interface.get_advisory_for_flight_plan())
	# pprz_UTM_interface.get_own_flights()
	# pprz_UTM_interface.get_flights_in_mission_airspace()
	# pprz_UTM_interface.test_telemtry()
	# pprz_UTM_interface.start_flight_comms()
