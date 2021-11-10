#!/usr/bin/python3

from PySide6 import QtCore, QtWidgets, QtGui

class CancelFlightCreationConfirmationDialog(QtWidgets.QDialog):

	def __init__(self):

		super().__init__()

		self.setWindowTitle("Flight creation cancelation confirmation")

		msg = QtWidgets.QLabel("You want to cancel current flight creation. Confirm?")

		buttons = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

		self.button_box = QtWidgets.QDialogButtonBox(buttons)
		self.button_box.accepted.connect(self.accept)
		self.button_box.rejected.connect(self.reject)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(msg)
		self.layout.addWidget(self.button_box)
		self.setLayout(self.layout)