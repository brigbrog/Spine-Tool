# Window Manager 

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

# from spine_tool import SpineTool
# from layout_objects import ImageWindow

# class WindowManager(ImageWindow):
class WindowManager: 
    # Window Manager for SpineToolApp
    def __init__(self, appManager):
        
        self.appManager = appManager
        # super().__init__()
        self._initUI()

    def _initUI(self):
        #
        self.appManager.graphicsView = QGraphicsView()
        self.appManager.setCentralWidget(self.appManager.graphicsView)
        
        self._createImageToolBar()
        self._createStatusBar()


# FEATURES
    def _createImageToolBar(self):
        # should include conversion widgets and convert button ONLY

        functions = QToolBar()

        # ToolBar Buttons
        load_button = self._getLoadImageButton()
        convert_button = self._getConvertImageButton() 
        export_button = self._getExportImageButton()

        # Add Widgets to ToolBar
            # create menu bar for file i/o
        functions.addWidget(load_button)
        functions.addWidget(convert_button)
        functions.addWidget(export_button)
        self.appManager.addToolBar(Qt.ToolBarArea.LeftToolBarArea, functions)

    def _createMenu(self):
        menubar = self.appManager.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu("&Menu")
        file_menu.addAction("&Exit", self.close)
        # other menu actions

    def _createToolBar(self):
        tools = self.appManager.QToolBar()
        tools.addAction("Exit", self.close)
        self.appManager.addToolBar(tools)
        
    def _createStatusBar(self, message = "Status Bar"):
        status = QStatusBar()
        status.showMessage(message)
        self.appManager.setStatusBar(status)

    def _createFunctionBar(self):
        functions = QToolBar()
        self.appManager.addToolBar(Qt.ToolBarArea.LeftToolBarArea, functions)


# BUTTONS
    def _getLoadImageButton(self):
        # will be moved to menu bar

        load_button = QPushButton("LODE")
        load_button.clicked.connect(self.appManager._loadImage)

        return load_button

    def _getConvertImageButton(self):

        convert_button = QPushButton("Connvert")
        convert_button.clicked.connect(self.appManager._convertImage)

        return convert_button

    def _getExportImageButton(self):
        # will be moved to menu bar

        export_button = QPushButton("Ecksport")
        export_button.clicked.connect(self.appManager._exportImage)

        return export_button
