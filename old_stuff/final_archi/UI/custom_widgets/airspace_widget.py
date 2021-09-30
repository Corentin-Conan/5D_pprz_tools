#!/user/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui

class AirspaceWidget(QtWidgets.QWidget):

	def __init__(self, airspace):
		super().__init__()

		# format airspace : [name, type, x coord, y coord, color]
		self.name = airspace[0]
		self.type = airspace[1]
		self.color = airspace[4]
		if self.color == 'r':
			self.color = "RED"
		elif self.color == 'g':
			self.color = 'GREEN'
		elif self.color == 'b':
			self.color = "BLUE"
		elif self.color == 'c':
			self.color = "CYAN"
		elif self.color == 'm':
			self.color = "MAGENTA"
		elif self.color == 'y':
			self.color = "YELLOW"

		self.main_layout = QtWidgets.QVBoxLayout(self)
		self.box = QtWidgets.QGroupBox()
		self.main_layout.addWidget(self.box)
		self.layout = QtWidgets.QVBoxLayout()
		self.box.setLayout(self.layout)
		self.box.setFixedHeight(90)

		self.name_label = QtWidgets.QLabel(self.name)
		self.type_label = QtWidgets.QLabel(self.type)
		self.color_label = QtWidgets.QLabel(self.color)
		self.layout.addWidget(self.name_label)
		self.layout.addWidget(self.type_label)
		self.layout.addWidget(self.color_label)

