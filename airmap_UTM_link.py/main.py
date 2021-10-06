#!/usr/bin/python3

import sys
from PySide6 import QtCore, QtWidgets, QtGui

from UI import UI
from airmap_request_manager import AirmapRequestManager
from pprz_request_manager import PprzRequestManager

def main():
	app = QtWidgets.QApplication([])
	am_req_man = AirmapRequestManager()
	pprz_req_man = PprzRequestManager()
	ui = UI(am_req_man, pprz_req_man)
	ui.show()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()

