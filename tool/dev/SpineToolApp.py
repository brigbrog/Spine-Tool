'''
Developed by Brian Brogan
TOP-LEVEL run script for SpineTool
For SpineTool functions see spine_tool.py
November 2026
'''

import sys
from pathlib import Path

# from PyQt6.QtCore import Qt
# from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication#, QLabel, QMainWindow, QStatusBar, QToolBar

#sys.path.append("../../frameworks/_pyqt/framework/dev")
#sys.path.append("../../frameworks/_pyqt/framework/src")

# from layout_objects import Window, ImageWindow
from spine_tool import SpineTool


if __name__ == "__main__":

	app = QApplication([])

	window = SpineTool(windowTitle = "SpineTool (0.0)")
	
	window.show()
	sys.exit(app.exec())
