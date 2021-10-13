#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui



class AirspaceWidget(QtWidgets.QWidget):


	def __init__(self, _pprz_shape_id):

		super().__init__()

		# airspace params
		self.pprz_shape_id = _pprz_shape_id




class AirspaceTypeWidget(QtWidgets.QWidget):


	def __init__(self):

		super().__init__()