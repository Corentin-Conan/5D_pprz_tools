#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui

class FlightPlanConfirmationWindow(QtWidgets.QDialog):

	def __init__(self):
		super().__init__()
		self.setWindowModality(QtCore.Qt.ApplicationModal)
		self.resize(400, 800)
		self.setWindowTitle("Flight plan confirmation window")

		self.exit_code = 0

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

		self.label_time_format = QtWidgets.QLabel("Time format")
		self.time_format = QtWidgets.QLabel("yyyy-MM-dd'T'HH:mm:ss.SSSZ")

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
		self.main_box_layout.addRow(self.label_time_format, self.time_format)
		self.main_box_layout.addRow(self.label_flight_description, self.line_edit_flight_description)

		self.send_and_close_button = QtWidgets.QPushButton("Send and Close")
		self.send_and_close_button.clicked.connect(self.close_with_button)
		self.main_layout.addWidget(self.send_and_close_button)

	def close_with_button(self):
		self.exit_code = 1
		self.close()

	def set_fields_from_dict(self, dic):
		## /!\ make sure to keep the same names as the attributes of the airmap flight plan class /!\
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