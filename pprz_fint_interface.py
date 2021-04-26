#!/usr/bin/python3

import requests
import json
import sys
from os import path, getenv

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan

from msg_def import TelemetryMessage

class Pprz_FINT_Interface(object):

	def __init__(self, ivy_interface):
		self.username = "corentin.conan@enac.fr"
		self.password = "Xes2GEcSO3LmWfgU"
		self.auth_response = None
		self.TOKEN = None
		self.headers = None
		self.object_id = []

		self.cond_send_tele = False

		## connection to pprz
		self._interface = ivy_interface
		# self.pprzconnect = PprzConnect(notify=self.update_config, ivy=self._interface)
		self._interface.subscribe(self.send_tele, PprzMessage("ground", "FLIGHT_PARAM"))


	def log_in(self, username, password):
		user_payload = {
			'loginId': username, 
			'password': password
		}
		self.auth_response = requests.post(
			"https://api.5daerosafe.finot.cloud/auth/jwt/login",
			json = user_payload)

		if self.auth_response.status_code == 200:
			self.TOKEN = self.auth_response.json()["result"]["token"]
			print("User logged in")
			self.headers = {
				"X-Tenant": "5daerosafe",
				"Authorization": "JWT " + self.TOKEN 
			}
			return(1)
		else :
			print("User not logged in " + str(self.auth_response.text))
			return(0)


	def print_connexion_details(self):
		if self.TOKEN is not None:
			print(self.auth_response.text)
		else:
			print("User not logged in ")


	def send_test_object(self):
		# object = {
		# 	"type": "My5daerosafeObject",
		# 	"attributes": [
		# 		{
		# 			"name": "message",
		# 			"type": "Text",
		# 			"value": "Hello FINT"
		# 		}
		# 	]
		# }
		object = TelemetryMessage(1.0, 1.0, 1.0, 1.0)
		response = requests.post(
			"https://api.5daerosafe.finot.cloud/inventory/v1/objects",
			headers = self.headers,
			json = object.object)
		print(response.text)
		self.object_id.append(response.json()["result"]["object"]["id"])
		object = TelemetryMessage(2.0, 2.0, 2.0, 2.0)
		response = requests.post(
			"https://api.5daerosafe.finot.cloud/inventory/v1/objects",
			headers = self.headers,
			json = object.object)
		print(response.text)
		self.object_id.append(response.json()["result"]["object"]["id"])


	def retreive_test_object(self):
		response = requests.get(
			"https://api.5daerosafe.finot.cloud/inventory/v1/objects/?type=TelemetryReport",
			headers = self.headers)
		for obj in response.json()["result"]["object"]:
			self.object_id.append(obj["id"])
		print(response.text)

	def remove_test_object(self):
		for id in self.object_id:
			response = requests.delete(
				"https://api.5daerosafe.finot.cloud/inventory/v1/objects/" + id,
				headers = self.headers)
			print(response.status_code)

	def send_tele(self, msg_id, msg):
		if self.cond_send_tele:
			msg = TelemetryMessage(msg["lat"], msg["long"], msg["alt"], msg["unix_time"])
			response = requests.post(
				"https://api.5daerosafe.finot.cloud/inventory/v1/objects",
				headers = self.headers,
				json = msg.object)


def main():
	interface = Pprz_FINT_Interface()
	interface.log_in("corentin.conan@enac.fr", "Xes2GEcSO3LmWfgU")
	interface.send_test_object()
	interface.retreive_test_object()
	interface.remove_test_object()

if __name__ == '__main__':
	main()


