#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui

class FlightPlanConfirmationWindow(QtWidgets.QDialog):

	def __init__(self):
		super().__init__()
		self.setWindowModality(QtCore.Qt.ApplicationModal)
		self.resize(400, 800)
		self.setWindowTitle("Flight plan confirmation window")

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.main_box = QtWidgets.QGroupBox()
		self.main_layout.addWidget(self.main_box)
		self.main_box_layout = QtWidgets.QFormLayout()
		self.main_box.setLayout(self.main_box_layout)

		self.label_flight_plan_id = QtWidgets.QLabel("Flight plan ID")
		self.text_flight_plan_id = QtWidgets.QLabel()

		self.label_flight_id = QtWidgets.QLabel("Flight ID")
		self.text_flight_id = QtWidgets.QLabel()

		self.label_pilot_id = QtWidgets.QLabel("Pilot ID")
		self.text_pilot_id = QtWidgets.QLabel()

		self.label_aircraft_id = QtWidgets.QLabel("Aircraft ID")
		self.text_aircraft_id = QtWidgets.QLabel()

		self.label_take_off_lon = QtWidgets.QLabel("Take off longitude")
		self.line_edit_take_off_lon = QtWidgets.QLineEdit()

		self.label_take_off_lat = QtWidgets.QLabel("Take off latitude")
		self.line_edit_take_off_lat = QtWidgets.QLineEdit()

		self.label_min_alt_agl = QtWidgets.QLabel("Min altitude AGL")
		self.line_edit_min_alt_agl = QtWidgets.QLineEdit()

		self.label_max_alt_agl = QtWidgets.QLabel("Max altitude AGL")
		self.line_edit_max_alt_agl = QtWidgets.QLineEdit()

		self.label_buffer = QtWidgets.QLabel("Buffer")
		self.line_edit_buffer = QtWidgets.QLineEdit()

		self.label_start_time = QtWidgets.QLabel("Start time")
		self.line_edit_start_time = QtWidgets.QLineEdit()

		self.label_end_time = QtWidgets.QLabel("End time")
		self.line_edit_end_time = QtWidgets.QLineEdit()

		self.label_flight_description = QtWidgets.QLabel("Flight description")
		self.line_edit_flight_description = QtWidgets.QTextEdit()

		self.main_box_layout.addRow(self.label_flight_plan_id, self.text_flight_plan_id)
		self.main_box_layout.addRow(self.label_flight_id, self.text_flight_id)
		self.main_box_layout.addRow(self.label_pilot_id, self.text_pilot_id)
		self.main_box_layout.addRow(self.label_aircraft_id, self.text_aircraft_id)
		self.main_box_layout.addRow(self.label_take_off_lon, self.line_edit_take_off_lon)
		self.main_box_layout.addRow(self.label_take_off_lat, self.line_edit_take_off_lat)
		self.main_box_layout.addRow(self.label_min_alt_agl, self.line_edit_min_alt_agl)
		self.main_box_layout.addRow(self.label_max_alt_agl, self.line_edit_max_alt_agl)
		self.main_box_layout.addRow(self.label_buffer, self.line_edit_buffer)
		self.main_box_layout.addRow(self.label_start_time, self.line_edit_start_time)
		self.main_box_layout.addRow(self.label_end_time, self.line_edit_end_time)
		self.main_box_layout.addRow(self.label_flight_description, self.line_edit_flight_description)

	def set_fields(self, fp_id = None, flight_id = None, pilot_id = None, ac_id = None, 
		take_off_lon = None, take_off_lat = None, min_alt = None, max_alt = None, buf = None,
		start_time = None, end_time = None, flight_descr = None, geometry = None):
	## /!\ make sure to keep the same names as the attributes of the airmap flight plan class /!\
		if fp_id is not None:
			self.text_flight_plan_id.setText(fp_id)
		if flight_id is not None:
			self.text_flight_id.setText(flight_id)
		if pilot_id is not None:
			self.text_pilot_id.setText(pilot_id)
		if ac_id is not None:
			self.text_aircraft_id.setText(ac_id)
		if take_off_lon is not None:
			self.line_edit_take_off_lon.setText(take_off_lon)
		if take_off_lat is not None:
			self.line_edit_take_off_lat.setText(take_off_lat)
		if min_alt is not None:
			self.line_edit_min_alt_agl.setText(min_alt)
		if max_alt is not None:
			self.line_edit_max_alt_agl.setText(max_alt)
		if buf is not None:
			self.line_edit_buffer.setText(buf)
		if start_time is not None:
			self.line_edit_start_time.setText(start_time)
		if end_time is not None:
			self.line_edit_end_time.setText(end_time)
		if flight_descr is not None:
			self.line_edit_flight_description.setText(flight_descr)

	def set_fields_from_dict(self, dic):
		for elem in dic:
			if dic[elem] is not None:
				if elem == "fp_id":
					self.text_flight_plan_id.setText(str(dic[elem]))
				if elem == "flight_id" :
					self.text_flight_id.setText(str(dic[elem]))
				if elem == "pilot_id":
					self.text_pilot_id.setText(str(dic[elem]))
				if elem == "ac_id":
					self.text_aircraft_id.setText(str(dic[elem]))
				if elem == "take_off_lon":
					self.line_edit_take_off_lon.setText(str(dic[elem]))
				if elem == "take_off_lat":
					self.line_edit_take_off_lat.setText(str(dic[elem]))
				if elem == "min_alt":
					self.line_edit_min_alt_agl.setText(str(dic[elem]))
				if elem == "max_alt":
					self.line_edit_max_alt_agl.setText(str(dic[elem]))
				if elem == "buf":
					self.line_edit_buffer.setText(str(dic[elem]))
				if elem == "start_time":
					self.line_edit_start_time.setText(str(dic[elem]))
				if elem == "end_time":
					self.line_edit_end_time.setText(str(dic[elem]))
				if elem == "flight_descr":
					self.line_edit_flight_description.setText(str(dic[elem]))
				if elem == "geometry":
					pass

	def get_values(self):
		dict_val = {}
		dict_val["fp_id"] = self.text_flight_plan_id.text()
		dict_val["flight_id"] = self.text_flight_id.text()
		dict_val["pilot_id"] = self.text_pilot_id.text()
		dict_val["ac_id"] = self.text_aircraft_id.text()
		dict_val["take_off_lon"] = self.line_edit_take_off_lon.text()
		dict_val["take_off_lat"] = self.line_edit_take_off_lat.text()
		dict_val["min_alt"] = self.line_edit_min_alt_agl.text()
		dict_val["max_alt"] = self.line_edit_max_alt_agl.text()
		dict_val["buf"] = self.line_edit_buffer.text()
		dict_val["start_time"] = self.line_edit_start_time.text()
		dict_val["end_time"] = self.line_edit_end_time.text()
		dict_val["flight_descr"] = self.line_edit_flight_description.toPlainText()
		return dict_val