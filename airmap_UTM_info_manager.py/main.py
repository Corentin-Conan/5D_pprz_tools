#!/usr/bin/python3

import sys
from PySide6 import QtCore, QtWidgets, QtGui

from UI import UI

def main():
	app = QtWidgets.QApplication([])
	ui = UI()
	ui.show()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()

