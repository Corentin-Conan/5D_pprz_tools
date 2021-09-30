#!/usr/bin/python3

from UI.UI import UI
from UI.waterway_inspection_GGCS import WaterwayInspectionGGCS
from UI.end_user_UI import EndUserUI
from request_managers.request_manager import RequestManager

from PySide6 import QtCore, QtWidgets, QtGui
import sys

def main():
	request_manager = RequestManager()
	app = QtWidgets.QApplication([])
	# ui = UI(request_manager)
	# ui = WaterwayInspectionGGCS(request_manager)
	ui = EndUserUI()
	ui.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()