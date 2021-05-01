#!/usr/bin/python3

from .user_profile.fint_profile import FINTUserProfile

import requests
import json
import threading
import time

class FintRequestManager(object):

	def __init__(self):
		super().__init__()
		self.fint_user_profile = FINTUserProfile()

	def update_credentials(self, user_name, password):
		self.fint_user_profile.user_name = user_name
		self.fint_user_profile.password = password

	def log_in(self, connection_status_label):
		print("\nLogging in ...")
		user_payload = {
			'loginId': self.fint_user_profile.user_name, 
			'password': self.fint_user_profile.password
		}
		self.auth_response = requests.post(
			"https://api.5daerosafe.finot.cloud/auth/jwt/login",
			json = user_payload)
		if self.auth_response.status_code == 200:
			self.fint_user_profile.token = self.auth_response.json()["result"]["token"]
			self.fint_user_profile.refresh_token = self.auth_response.json()["result"]["refreshToken"]
			print("User logged in to FINT API")
			connection_status_label.setStyleSheet("color: rgb(50,200,50)")
			connection_status_label.setText("Connected")
			refresh_thread = threading.Thread(target = self.thread_refresh, 
				args = (3600 - 100, connection_status_label,), 
				daemon = True)
			refresh_thread.start()
		else :
			print("User not logged in " + str(self.auth_response.text))
			connection_status_label.setStyleSheet("color: rgb(255,0,0)")
			connection_status_label.setText("Not Connected")

	def thread_refresh(self, refresh_timer, connection_status_label):
		## thread meant to refresh the FINT access token
		while(True):
			time.sleep(refresh_timer)
			print("\nAutomatic FINT token refresh ...")
			connection_status_label.setStyleSheet("color: rgb(150,150,150)")
			connection_status_label.setText("Refreshing Token")
			URL = "https://api.5daerosafe.finot.cloud/auth/jwt/refresh"
			PAYLOAD = {
				'refreshToken': self.fint_user_profile.refresh_token
			}
			resp = requests.post(URL, json=PAYLOAD)
			if resp.status_code == 200:
				print("Automatic token refresh success")
				self.fint_user_profile.token = resp.json()["result"]["token"]
				connection_status_label.setStyleSheet("color: rgb(50,200,50)")
				connection_status_label.setText("Connected")
			else:
				print("Failing to refresh token ; status code = " + str(resp.status_code))
				connection_status_label.setStyleSheet("color: rgb(255,0,0)")
				connection_status_label.setText("Refresh Token Failed")
