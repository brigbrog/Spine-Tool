'''
Developed by Brian Brogan
app construction for SpineTool
November 2026
'''

import sys
import os
# from pathlib import Path

# import seaborn as sns
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
# from matplotlib.figure import Figure

import numpy as np
import pandas as pd
# from PIL import Image

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage #, QAction, QIcon, QKeySequence, 

from PyQt6.QtWidgets import (
	# QWidget,
	# QVBoxLayout,
	# QApplication,
	# QLabel,
	QMainWindow,
	# QStatusBar,
	# QToolBar,
	# QGraphicsView,
	# QPushButton,
	QFileDialog,
	QGraphicsScene,
	QGraphicsPixmapItem
	)

from window_manager import WindowManager
from data_manager import DataManager

"""
NOTES :
------------------------------------------------------------------------------------------------

VIEWPORT RESIZE needs attention, weird padding behavior


"""

class SpineTool(QMainWindow):
# Initialization
	def __init__(self, windowTitle = "SpineTool", windowWidth = 1200, windowHeight = 600):
		super().__init__(parent=None)

		self.windowWidth = windowWidth
		self.windowHeight = windowHeight
		self.resize(self.windowWidth, self.windowHeight)
		self.setWindowTitle(windowTitle)
		self.scene = None

		# I / O Fields
		self.originPath = None
		self.currentAnalysisType = None

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


	def _runAnalysis(self, analysisParams):
		'''
		analysisParams {"analysisType": str, "analysisParams": dict}
		'''
		if self.dataManager.data is None:
			self.statusBar().showMessage("LOAD DATA BEFORE RUNNING ANALYSIS")
			return

		self.dataManager._runAnalysis(**analysisParams)


	def _plotAnalysis(self, analysisType):
		'''
		'''
		if self.dataManager.data is None:
			self.statusBar().showMessage("LOAD DATA BEFORE PLOTTING ANALYSIS")
			return

		plotArr = self.dataManager._plotAnalysis(analysisType)
		if plotArr is None:
			self.statusBar().showMessage("RUN ANALYSIS BEFORE PLOTTING")
		else:
			self._loadPlotArr(plotArr)


	def _clearViewPort(self):
		scene = self.graphicsView.scene()
		if scene is not None:
			scene.clear()


	def _loadPlotArr(self, plotArr):
		self._clearViewPort()

		vp = self.graphicsView.viewport()
		dpr = vp.devicePixelRatioF()
		test_qimg = self.dataManager._ndarray2QImage(plotArr)
		test_qimg.setDevicePixelRatio(dpr)

		pixmap = QPixmap.fromImage(test_qimg)
		self._reloadCanvas(pixmap)


	def _loadTestImage(self):
		self._clearViewPort()

		vp = self.graphicsView.viewport()
		dpr = vp.devicePixelRatioF()
		vp_w = max(1, int(round(vp.width())))
		vp_h = max(1, int(round(vp.height())))

		# print(f"width: {vp_w} (dpr={dpr})")
		# print(f"height: {vp_h} (dpr={dpr})")

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
		self.originPath = fpath
		try:
			self.dataManager._unloadData()
			self.dataManager._initData(fpath)
			self.dataManager._cleanBranchData()
			print(f"{self.dataManager.data.head()}")
		except ValueError:
			self.statusBar().showMessage("SELECTED DATA DIRECTORY IS INVALID")


	def _exportData(self):
		'''
		'''
		fname = None
		data = None

		if self.currentAnalysisType is None:
			self.statusBar().showMessage("PERFORM ANALYSIS BEFORE ATTEMPTING TO EXPORT")
			return
		elif self.currentAnalysisType == 'nn':
			fname = os.path.basename(self.originPath) + '_nearest_neighbors'
			data = self.dataManager.nnData
		elif self.currentAnalysisType == 'dbscan':
			fname = os.path.basename(self.originPath) + '_DBSCAN'
			data = self.dataManager.dbscanData
		elif self.currentAnalysisType == 'ripley':
			fname = os.path.basename(self.originPath) + '_ripley'
			data = self.dataManager.ripleyData
		elif self.currentAnalysisType == 'kde':
			fname = os.path.basename(self.originPath) + '_kde'
			data = self.dataManager.kdeData

		if fname is None:
			return
		else:
			fpath = QFileDialog.getExistingDirectory(
				self, "Select Directory", ""
			)
			save_path = os.path.join(fpath, fname+".csv")

			data.to_csv(save_path)


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