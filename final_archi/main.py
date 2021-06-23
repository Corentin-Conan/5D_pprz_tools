#!/usr/bin/python3

from UI.end_user_UI import EndUserUI
from controler import Controler
# from request_managers.request_manager import RequestManager

from PySide6 import QtCore, QtWidgets, QtGui
import sys

def main():
	# request_manager = RequestManager()
	app = QtWidgets.QApplication([])
	controler = Controler()
	ui = EndUserUI(controler)
	ui.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()