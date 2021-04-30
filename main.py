#!/usr/bin/python3

from UI.UI import UI
from request_managers.request_manager import RequestManager

from PySide6 import QtCore, QtWidgets, QtGui
import sys

def main():
	request_manager = RequestManager()
	app = QtWidgets.QApplication([])
	ui = UI(request_manager)
	ui.resize(1400, 900)
	ui.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()