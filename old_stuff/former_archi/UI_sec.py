#!/usr/bin/python3

from pprz_airmap_interface import Pprz_UTM_Interface
from telemetry_interface import TelemetryInterface
import sys
from os import path, getenv
import json
from PySide6 import QtCore, QtWidgets, QtGui
from outlog import OutLog

PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.dirname(path.abspath(__file__))))
sys.path.append(PPRZ_HOME + "/var/lib/python")
sys.path.append(PPRZ_HOME + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from pprz_connect import PprzConnect
from flight_plan import FlightPlan


class UTM_UI(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()
		#creates the ivy interface (must be unique)
		self.interface = IvyMessagesInterface("msgInterface")
		# create a Pprz_UTM_Interface object
		self.pprz_UTM_interface = Pprz_UTM_Interface(self.interface)
		# create the UI
		self.layout = QtWidgets.QVBoxLayout(self)
		self.textEdit = QtWidgets.QTextEdit()
		self.layout.addWidget(self.textEdit)
		sys.stdout = OutLog(self.textEdit, sys.stdout)

		self.pprz_UTM_interface.log_in(
			"2cd97349-096e-4457-be5d-bd1e751380ef", 
			"corentin.conan@enac.fr",
			"Z&8r3m8xxXR_Ap-")

		#creates a telemetry interface object
		self.telemetry_interface = TelemetryInterface(self.interface)
		self.telemetry_interface.authentify(self.pprz_UTM_interface.TOKEN)

if __name__ == '__main__':
	print('test')
	app = QtWidgets.QApplication([])
	utm_ui = UTM_UI()
	utm_ui.resize(800, 600)
	utm_ui.show()
	sys.exit(app.exec_())

