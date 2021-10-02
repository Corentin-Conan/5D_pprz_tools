#!/usr/bin/python3

import sys

from PySide6 import QtCore, QtWidgets, QtGui

from outlog import OutLog


class UI(QtWidgets.QWidget):

	def __init__(self):

		super().__init__()

		self.setWindowTitle("Airmap Information Manager")
		self.resize(600, 800)

		# main layout
		self.main_layout = QtWidgets.QVBoxLayout(self)

		# top box - login
		self.login_box = QtWidgets.QGroupBox("Airmap API Connexion")
		self.main_layout.addWidget(self.login_box)
		self.login_box.setFixedHeight(150)

		# main section - information management
		self.main_box = QtWidgets.QGroupBox("UTM Link")
		self.main_layout.addWidget(self.main_box)
		self.main_box_layout = QtWidgets.QHBoxLayout()
		self.main_box.setLayout(self.main_box_layout)

		# bottom box - outlog
		self.out_log = QtWidgets.QTextEdit()
		self.out_log.setFixedHeight(150)
		self.font = QtGui.QFont()
		self.font.setPointSize(8)
		self.out_log.setFont(self.font)
		self.main_layout.addWidget(self.out_log)
		sys.stdout = OutLog(self.out_log, sys.stdout)

		# left box 
		# ..

		# right box
		# ..