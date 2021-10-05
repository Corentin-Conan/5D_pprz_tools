#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui



class FlightPlanWidget(QtWidgets.QWidget):


	def __init__(self, _flight):

		super().__init__()

		self.flight = _flight

		self.id = self.flight["id"]
		self.lat = self.flight["latitude"]
		self.lon = self.flight["longitude"]
		self.ac_id = self.flight["aircraft_id"]

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.box = QtWidgets.QGroupBox()
		self.main_layout.addWidget(self.box)
		self.layout = QtWidgets.QVBoxLayout()
		self.box.setLayout(self.layout)

		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.setFont(self.font)

		self.id_label = QtWidgets.QLabel("ID : " + self.id)
		self.latlon_label = QtWidgets.QLabel("Lat : " + str(self.lat) + " ; Lon : " + str(self.lon))
		self.ac_id_label = QtWidgets.QLabel("Aircraft : " + self.ac_id)

		self.layout.addWidget(self.id_label)
		self.layout.addWidget(self.latlon_label)
		self.layout.addWidget(self.ac_id_label)

