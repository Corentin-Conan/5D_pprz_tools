#!/usr/bin/python3

from UI.end_user_UI import EndUserUI
from mission_manager import MissionManager
from UI.DMO_DSO_UI import DMODSOUI
from request_managers.request_manager import RequestManager

from PySide6 import QtCore, QtWidgets, QtGui
import sys

def main():
	request_manager = RequestManager()
	app = QtWidgets.QApplication([])
	mission_manager = MissionManager()
	ui = EndUserUI(mission_manager, request_manager)
	ui.show()
	ui2 = DMODSOUI(mission_manager, request_manager)
	# ui2.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()