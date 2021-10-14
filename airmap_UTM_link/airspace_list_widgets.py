#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui



class AirspaceWidget(QtWidgets.QWidget):


	def __init__(self, _pprz_shape_id, airspace):

		super().__init__()

		# airspace params
		self.pprz_shape_id = _pprz_shape_id
		self.json_airspace = airspace
		self.name = airspace["name"]
		self.type = airspace["type"]
		self.geometry_type = airspace['geometry']['type'] 
		self.coordinates = airspace['geometry']['coordinates']

		# representation
		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.checkbox = QtWidgets.QCheckBox(self.name)
		self.main_layout.addWidget(self.checkbox)
		


class AirspaceTypeWidget(QtWidgets.QWidget):


	def __init__(self, _type, _child = None):

		super().__init__()

		# airspace type params
		self.type = _type

		if _child is not None:

			self.children = [_child]

		else:

			self.children = []

		# representation
		self.main_layout = QtWidgets.QFormLayout(self)

		self.label_type = QtWidgets.QLabel(self.type.upper())
		self.main_chkbox = QtWidgets.QCheckBox("")
		self.main_layout.addRow(self.label_type, self.main_chkbox)

		self.main_box = QtWidgets.QGroupBox()
		self.main_layout.addRow(self.main_box)
		self.layout = QtWidgets.QVBoxLayout(self.main_box)

		for child in self.children:

			self.layout.addWidget(child)


	def add_child(self, child):

		self.children.append(child)

		self.layout.addWidget(child)



