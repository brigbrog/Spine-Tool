'''
Developed by Brian Brogan
app construction for SpineTool
November 2026
'''

import sys
import os
from pathlib import Path

import seaborn as sns
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
# from matplotlib.figure import Figure

import numpy as np
from PIL import Image

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWidgets import (
	QApplication,
	QLabel,
	QMainWindow,
	QStatusBar,
	QToolBar,
	QGraphicsView,
	QPushButton,
	QFileDialog,
	QGraphicsScene,
	QGraphicsPixmapItem
	)

from window_manager import WindowManager
from data_manager import DataManager

"""
NOTES :
------------------------------------------------------------------------------------------------

"""

class SpineTool(QMainWindow):
# Initialization
	def __init__(self, windowTitle = "SpineTool", windowWidth = 1200, windowHeight = 600):
		# super().__init__()
		super().__init__(parent=None)

		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.resize(self.windowWidth, self.windowHeight)
		self.setWindowTitle(windowTitle)
		self.scene = None

		# initialize front-end
		self.windowManager = WindowManager(self)
		# initialize back-end
		self.dataManager = DataManager(self)




# ACTIONS :
# ------------------------------------------------------------------------------------------------

	def _placeHolder(self):
		'''
		fake method for place holding in feature design
		'''
		return

	def _runAnalysis(self, analysisType):
		'''
		'''
		print(f'running {analysisType}...')
		self.dataManager._runAnalysis(analysisType)

	def _plotAnalysis(self, analysisType):
		'''
		'''
		print(f'plotting {analysisType}...')
		self.dataManager._plotAnalysis(analysisType)


	def _clearViewPort(self):
		scene = self.graphicsView.scene()
		if scene is not None:
			scene.clear()


	def _loadTestImage(self):
		self._clearViewPort()

		vp = self.graphicsView.viewport()
		dpr = vp.devicePixelRatioF()  # e.g., 1.0 on standard displays, 2.0 on Retina/HiDPI
		vp_w = max(1, int(round(vp.width() * dpr)))
		vp_h = max(1, int(round(vp.height() * dpr)))

		print(f"width: {vp_w} (dpr={dpr})")
		print(f"height: {vp_h} (dpr={dpr})")

		# Generate RGBA uint8 directly (0..255) with opaque alpha channel
		test_cimg = np.random.randint(0, 256, size=(vp_h, vp_w, 3), dtype=np.uint8)
		test_aimg = np.full((vp_h, vp_w, 1), 255, dtype=np.uint8)
		test_img = np.concatenate([test_cimg, test_aimg], axis=2)

		test_qimg = self.dataManager._ndarray2QImage(test_img)
		test_qimg.setDevicePixelRatio(dpr)

		pixmap = QPixmap.fromImage(test_qimg)
		self._reloadCanvas(pixmap)


	def _loadData(self):
		'''
		'''
		self.statusBar().showMessage("SELECT DATA DIRECTORY")
		fpath = QFileDialog.getExistingDirectory(
				self, "Select Directory", ""
			)
		if not fpath:
			return

		try:
			self.dataManager._unloadData()
			self.dataManager._initData(fpath)
		except ValueError:
			self.statusBar().showMessage("SELECTED DATA DIRECTORY IS INVALID")


	def _reloadCanvas(self, pixmap: QPixmap):
		# reloads the graphics view with a new pixmap
		if self.scene is None:
			self.scene = QGraphicsScene(self)
			self.graphicsView.setScene(self.scene)
		else:
			self.scene.clear()

		self.pixmap_item = QGraphicsPixmapItem(pixmap)
		self.scene.addItem(self.pixmap_item)
		self.graphicsView.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)