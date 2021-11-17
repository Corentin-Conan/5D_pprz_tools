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
		
		self.checkbox.stateChanged.connect(self.show_or_del_shape)
		# self.checkbox.stateChanged.connect(self.print_rules)


	def show_or_del_shape(self):

		# TODO get ui cleaner way
		ui = self.parent().parent().parent().parent().parent().parent().parent().parent()

		pprz_req_manager = ui.pprz_request_manager

		pprz_req_manager.show_airspace_on_gcs(self)


	# # for testing purposes, to rework
	# def print_rules(self):

	# 	ui = self.parent().parent().parent().parent().parent().parent().parent().parent()

	# 	airmap_request_manager = ui.airmap_request_manager

	# 	# airmap_request_manager.get_rules_for_ruleset("5D AeroSafe")




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

		self.main_chkbox.stateChanged.connect(self.state_changed)

		self.main_box = QtWidgets.QGroupBox()
		self.main_layout.addRow(self.main_box)
		self.layout = QtWidgets.QVBoxLayout(self.main_box)

		for child in self.children:

			self.layout.addWidget(child)


	def add_child(self, child):

		self.children.append(child)

		self.layout.addWidget(child)



	def state_changed(self, int):

		if self.main_chkbox.isChecked():

			for child in self.children:

				child.checkbox.setChecked(True)

		else:

			for child in self.children:

				child.checkbox.setChecked(False)