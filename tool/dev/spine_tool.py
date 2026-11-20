'''
Developed by Brian Brogan
app construction for KnitKit
For knitkit run see KnitKitApp.py
November 2026
'''

import sys
import os
from pathlib import Path

import numpy as np
from PIL import Image

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QImage
from PyQt6 import QtWidgets
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

# sys.path.append("../../frameworks/_pyqt/framework")

# from layout_objects import Window, ImageWindow
from window_manager import WindowManager
from data_manager import DataManager

"""
NOTES :
------------------------------------------------------------------------------------------------

- Put Load, Export (change to Download ? ) in menu bar, leave image tool bar for transformation
	widgets and convert button

- create transformation widgets 
	(
		integer text entry : number of rows (nrows)
		checkbox : invert image
		slider : grid resolution (use automatic ranging for bounds around squareness)
		slider : grid shift, x & y
		slider : contrast threshold
	)

- Add multi channel support for image import

- Add multi format support for image export

- Update StatusBar functionality to display helpful messages when actions are completed

- automatic center detection ? 

- drag box ROI cropping ? :[]

"""

# class SpineTool(ImageWindow):
class SpineTool(QMainWindow):
# Initialization
	def __init__(self, windowTitle = "SpineTool", windowWidth = 1200, windowHeight = 600):
		# super().__init__()
		super().__init__(parent=None)

		self.resize(windowWidth, windowHeight)
		self.setWindowTitle(windowTitle)
		self.scene = None

		self._initUI()


	def _initUI(self):

		self.windowManager = WindowManager(self)
		self.dataManager = DataManager(self)


# ACTIONS :
# ------------------------------------------------------------------------------------------------

	def _placeHolder(self):
		'''
		fake method for place holding in feature design
		'''
		return


	def _loadData(self):
		'''
		'''
		self.statusBar().showMessage("SELECT DATA DIRECTORY")
		fpath = QFileDialog.getExistingDirectory(
				self, "Select Directory", ""
			)
		if not fpath:
			return

		for file in os.listdir(fpath):
			print(file)


	def _loadImage(self):
		'''
		add multi channel support
		'''
		self.statusBar().showMessage("SELECT IMAGE")
		fpath, _ = QFileDialog.getOpenFileName(
				self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)"
			)
		if not fpath:
			return

		image_pil = Image.open(fpath)
		image_pil = image_pil.convert("L")

		im_data = image_pil.tobytes("raw", "L")
		qimage = QImage(
			im_data, 
			image_pil.width,
			image_pil.height, 
			image_pil.width, 
			QImage.Format.Format_Grayscale8
		)

		pixmap = QPixmap.fromImage(qimage)
		self._reload_canvas(pixmap)
		self.statusBar().showMessage("IMAGE LOADED")


	def _exportImage(self):

		# check if scene is void
		if not self.scene:
			self.statusBar().showMessage("VOID SCENE")
			return None
		
		# prompt to select save path
		self.statusBar().showMessage("SELECT SAVE")
		fpath, _ = QFileDialog.getSaveFileName(
				self, "Select Save Location", "", "PNG Files (*.png)"
			)
		if not fpath:
			return

		image_q = self._pullScene()
		image_pil = self.dataManager._qImage2Pil(image_q)

		image_pil.save(fpath, "PNG")
		self.statusBar().showMessage(f"IMAGE SAVED TO {fpath}")


	def _pullScene(self):
		'''
		Pulls data from the scene <GraphicsView> and converts it to a QImage

		Params:
			None
		Returns:
			<QImage> of the data present in the scene GraphicsView
		'''
		# search for pixmap items in the scene
		pixmap_item = None
		for item in self.scene.items():
			if isinstance(item, QGraphicsPixmapItem):
				pixmap_item = item
				break
		# if no pixmap item was found in the scene, return None
		if not pixmap_item:
			return None

		# convert the pixmap item to a QImage
		pixmap = pixmap_item.pixmap()
		qimage = pixmap.toImage()

		return qimage


	def _convertImage(self):
		'''
		Converts the current image in <self.GraphicsView> with the HARD-CODED transformation. After converting the 
		canvas is reloaded. The original image is not preserved. If canvas is empty, returns None

		Params:
			None
		Returns:
			None
		
		'''
		if not self.scene:
			self.statusBar().showMessage("VOID SCENE")
			return None
		else:
			image_q = self._pullScene()
			image_pil = self.dataManager._qImage2Pil(image_q)
			image = np.array(image_pil)

			# transform
			new_image = self.dataManager._scramble(image)

			# QImage
			qimage = self.dataManager._ndarray2QImage(new_image)
			pix_im = QPixmap(qimage)

			# RELOAD
			self._reload_canvas(pix_im)
			self.statusBar().showMessage("SCRAMBLED !!!")


	def _reload_canvas(self, pixmap: QPixmap):
		# reloads the graphics view with a new pixmap
		if self.scene is None:
			self.scene = QGraphicsScene(self)
			self.graphicsView.setScene(self.scene)
		else:
			self.scene.clear()

		self.pixmap_item = QGraphicsPixmapItem(pixmap)
		self.scene.addItem(self.pixmap_item)
		self.graphicsView.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)

