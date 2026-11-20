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
        
        #self._createImageToolBar()

        # create the menu
        menuBar = self.appManager.menuBar()
        menuBar.setNativeMenuBar(False)
        self._buildMenu(menuBar)

        # self._createIOMenu()
        # self._createAnalysisMenu()
        
        # create Status bar
        self._createStatusBar()


# FEATURES
    def _buildMenu(self, menuBar):
        menu_definitions = [
            (
                "&Menu",
                [
                    (   
                        "Load Data",
                        self.appManager._loadData,
                        "Ctrl+O",
                        "Select a folder to import spine data from (must only contain *.csv)."
                    ),
                    (   
                        "Export",
                        self.appManager._placeHolder,
                        "Ctrl+S",
                        "Select a save location and specify a filename for the analysis data."
                    ),
                    None,  # separator
                    ("&Exit", self.appManager.close, "Ctrl+Q", "Close Spine Tool"), # <- handle this signal for confirmation
                ],
            ),
            (
                "&Analyze",
                [
                    ("Spine Visualizer", self.appManager._placeHolder, None, "Open Spine Visualizer"), # <- change to spine visualizer
                    ("Nearest Neighbors", self.appManager._placeHolder, None, "Open Nearest Neighbors"), # <- change to nearest neighbors
                    ("DBSCAN Clusters", self.appManager._placeHolder, None, "Open DBSCAN"), # <- change to clusters DBSCAN
                    ("Ripley K-Function", self.appManager._placeHolder, None, "Open Ripley K-Function"), # <- change to clusters DBSCAN
                    ("Kernel Density Estimate", self.appManager._placeHolder, None, "Open KDE"), # <- change to gaussian KDE
                    # ("")
                ],
            ),
        ]

        for menu_title, entries in menu_definitions:
            menu = menuBar.addMenu(menu_title)
            for entry in entries:
                if entry is None:
                    menu.addSeparator()
                    continue

                label, callback, shortcut, statusTip = entry
                action = menu.addAction(label, callback)
                if shortcut:
                    action.setShortcut(shortcut)
                if statusTip:
                    action.setStatusTip(statusTip)

    def _createSpineVisualizer(self):
        pass

    def _createNearestNeighborsToolBar(self):
        pass

    def _createDBSCANClustersToolBar(self):
        pass

    def _createRipleyKFunctionToolBar(self):
        pass

    def _createKenelDensityEstimateToolBar(self):
        pass

    def _clearToolbar(self):
        pass




    def _createImageToolBar(self):
        # should include conversion widgets and convert button ONLY

        functions = QToolBar()

        # ToolBar Buttons
        #load_button = self._getLoadImageButton()
        convert_button = self._getConvertImageButton() 
        #export_button = self._getExportImageButton()

        # Add Widgets to ToolBar
            # create menu bar for file i/o
        #functions.addWidget(load_button)
        functions.addWidget(convert_button)
        #functions.addWidget(export_button)
        self.appManager.addToolBar(Qt.ToolBarArea.LeftToolBarArea, functions)

    def _createIOMenu(self):
        menubar = self.appManager.menuBar()
        menubar.setNativeMenuBar(False)
        file_menu = menubar.addMenu("&Menu")
        
        file_menu.addAction("Load Data", self.appManager._loadData)
        file_menu.addAction("&Exit", self.appManager.close)


    def _createAnalysisMenu(self):
        menubar = self.appManager.menuBar()
        menubar.setNativeMenuBar(False)
        analysis_menu = menubar.addMenu("Analyze")

        analysis_menu.addAction("Nearest Neighbors",self.appManager.close)



    def _createToolBar(self):
        tools = self.appManager.QToolBar()
        tools.addAction("Exit", self.close)
        self.appManager.addToolBar(tools)
        
    def _createStatusBar(self, message = "STATUS"):
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

