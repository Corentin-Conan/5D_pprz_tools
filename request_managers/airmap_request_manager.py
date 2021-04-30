#!/usr/bin/python3

from .user_profile.airmap_profile import AirmapUserProfile

import requests
import json
import threading
import time

class AirmapRequestManager(object):

	def __init__(self):
		super().__init__()
		self.airmap_user_profile = AirmapUserProfile()


	def update_credentials(self, client_id, user_name, password):
		self.airmap_user_profile.client_id = client_id
		self.airmap_user_profile.user_name = user_name
		self.airmap_user_profile.password = password

	def log_in(self, connection_status_label):
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
			print("User logged in")
			connection_status_label.setStyleSheet("color: rgb(50,200,50)")
			connection_status_label.setText("Connected")
			refresh_thread = threading.Thread(target = self.thread_refresh, 
				args = (self.auth_response.json()["expires_in"] - 17995, connection_status_label,), 
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
				print("Failing to refresh token ; status code = " + resp.status_code)
				connection_status_label.setStyleSheet("color: rgb(255,0,0)")
				connection_status_label.setText("Refresh Token Failed")


	def print_connection_detail(self):
		print("\nAPI Key : " + self.airmap_user_profile.api_key + "\nToken : " + self.airmap_user_profile.token)
		