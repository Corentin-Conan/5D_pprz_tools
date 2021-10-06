#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui



class FlightPlanWidget(QtWidgets.QWidget):


	def __init__(self, flight):

		super().__init__()

		# flight plan params
		self.flight_id = flight["id"]
		self.flight_plan_id = flight["flight_plan_id"]
		self.pilot_id = flight["pilot_id"]
		self.lat = flight["latitude"]
		self.lon = flight["longitude"]
		self.ac_id = flight["aircraft_id"]
		self.created_at = flight["created_at"]
		self.start_time = flight["start_time"]
		self.end_time = flight["end_time"]
		self.country = flight["country"]
		self.state = flight["state"]
		self.city = flight["city"]
		self.geometry = flight["geometry"]
		self.coordinates = flight["geometry"]["coordinates"][0]
		self.buffer = flight["buffer"]
		self.max_altitude = flight["max_altitude"]

		# representation in list item
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.box = QtWidgets.QGroupBox()
		self.main_layout.addWidget(self.box)
		self.layout = QtWidgets.QVBoxLayout()
		self.box.setLayout(self.layout)

		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.setFont(self.font)

		self.id_label = QtWidgets.QLabel("Location : " + self.state + " , " + self.city)
		self.latlon_label = QtWidgets.QLabel("Lat : " + str(self.lat) + " ; Lon : " + str(self.lon))
		self.ac_id_label = QtWidgets.QLabel("Scheduled at : " + self.start_time)

		self.layout.addWidget(self.id_label)
		self.layout.addWidget(self.latlon_label)
		self.layout.addWidget(self.ac_id_label)

 