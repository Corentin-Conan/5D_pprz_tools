#!/usr/bin/python3

import sys
from PySide6 import QtCore, QtWidgets, QtGui

from UI import UI
from airmap_request_manager import AirmapRequestManager

def main():
	app = QtWidgets.QApplication([])
	am_req_man = AirmapRequestManager()
	ui = UI(am_req_man)
	ui.show()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()

