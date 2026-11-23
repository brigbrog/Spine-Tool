'''
Developed by Brian Brogan
TOP-LEVEL run script for SpineTool
For SpineTool system see spine_tool.py
November 2026
'''

import sys
from PyQt6.QtWidgets import QApplication
from spine_tool import SpineTool

if __name__ == "__main__":

	# Run a PyQt6 Application
	app = QApplication([])

	# Create SpineTool
	window = SpineTool(
		windowTitle = "SpineTool (0.0)",
		windowWidth = 2000,
		windowHeight = 1000)

	# Create the user loop
	window.show()
	sys.exit(app.exec())