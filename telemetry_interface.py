#!/usr/bin/python3

import sys
from os import path, getenv

import grpc

import interfaces.src.py.telemetry.telemetry_pb2 as telemetry_pb2
import interfaces.src.py.telemetry.telemetry_pb2_grpc as telemetry_pb2_grpc

import interfaces.src.py.system.status_pb2 as status_pb2

from google.auth.transport import grpc as google_auth_transport_grpc

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan

class TelemetryInterface(object):

	def __init__(self, interface):
		super().__init__()
		# pprz subscriptions
		self._interface = interface
		# self._interface.subscribe(self.on_telemetry_received, PprzMessage('ground', 'FLIGHT_PARAM'))
		# telemetry storage
		self.tele_reports = []
		# gRPC channel
		self.channel = None
		self.stub = None
		# airmap auth
		self.TOKEN = None

	def on_telemetry_received(self, msg_id, msg):
		# when gRPC works, this fun will send telemetry to airmap
		# for now it will just store the msg in list tele_reports
		tele_report = {'roll': msg['roll'], 'pitch': msg['pitch'], 'heading': msg['heading'], 
			'lat': msg['lat'], 'long': msg['long'], 'speed': msg['speed'], 
			'course': msg['course'], 'alt': msg['alt'], 'climb': msg['climb'], 
			'agl': msg['agl'], 'time': msg['unix_time'], 'itow': msg['itow'], 
			'airspeed': msg['airspeed']}
		self.tele_reports.append(tele_report)
		print(tele_report)

	def authentify(self, token):
		self.call_credientials = grpc.access_token_call_credentials("authorization: Bearer "+ str(token))
		self.empty_channel_credentials = grpc.ssl_channel_credentials()
		self.channel_credentials = grpc.composite_channel_credentials(
			self.empty_channel_credentials,
			self.call_credientials)
		self.channel = grpc.secure_channel(
			target='api.airmap.com:443', credentials=self.channel_credentials)
		# print(self.channel.ChannelConnectivity())
		self.stub = telemetry_pb2_grpc.CollectorStub(self.channel)
		print(self.stub)
		#test connection
		status = status_pb2.Status()
		status.level = 1
		feature = self.stub.ConnectProvider(status)
		print(feature)
		self.channel.close()

		# self.TOKEN = token
		# channel_credentials = grpc.ChannelCredentials(token)
		# self.channel = google_auth_transport_grpc.secure_authorized_channel(
		# 	target='api.airmap.com:443', credentials=channel_credentials, request=None)
		# print(self.channel)
		# print(grpc.StatusCode(self.channel))
		# self.stub = telemetry_pb2_grpc.CollectorStub(self.channel)
		# print(self.stub)
		# #test connection
		# status = status_pb2.Status()
		# status.level = 1
		# # self.channel.close()
		# feature = self.stub.ConnectProvider(status)
		# print(feature)

