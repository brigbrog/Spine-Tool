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
    QGraphicsPixmapItem,
    QLineEdit
    )


class WindowManager: 
    # Window Manager for SpineToolApp
    def __init__(self, appManager):
        
        self.appManager = appManager
        self._initUI()


    def _initUI(self):
        #
        self.appManager.graphicsView = QGraphicsView()
        self.appManager.setCentralWidget(self.appManager.graphicsView)

        # create the menu
        menuBar = self.appManager.menuBar()
        menuBar.setNativeMenuBar(False)
        self._buildMenu(menuBar)

        # create Status bar
        self._createStatusBar()


# FEATURES

    def _createStatusBar(self, message = "STATUS"):
        status = QStatusBar()
        status.showMessage(message)
        self.appManager.setStatusBar(status)


    def _buildMenu(self, menuBar):
        '''
        Create the menu bar specifications and populate the menu bar
        '''
        # specify the menu features 
        menu_specs = [
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
                    (
                        "Hide ToolBar",
                        self._clearToolBar,
                        "None",
                        "None"
                    ),
                    None,  # separator
                    ("&Exit", self.appManager.close, "Ctrl+Q", "Close Spine Tool"), # <- handle this signal for confirmation
                ],
            ),
            (
                "&Analyze",
                [
                    ("Spine Visualizer", self._createSpineVisualizer, None, "Open Spine Visualizer"), 
                    ("Nearest Neighbors", self._createNearestNeighborsToolBar, None, "Open Nearest Neighbors"), 
                    ("DBSCAN Clusters", self._createDBSCANClustersToolBar, None, "Open DBSCAN"), 
                    ("Ripley K-Function", self._createRipleyKFunctionToolBar, None, "Open Ripley K-Function"), 
                    ("Kernel Density Estimate", self._createKenelDensityEstimateToolBar, None, "Open KDE"), 
                    # ("")
                ],
            ),
        ]

        # populate the menu based on the above menu specifications
        for menu_title, entries in menu_specs:
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

# TOOL BAR

    def _clearToolBar(self):
        '''
        '''
        for toolbar in self.appManager.findChildren(QToolBar):
            if self.appManager.toolBarArea(toolbar) == Qt.ToolBarArea.RightToolBarArea:
                self.appManager.removeToolBar(toolbar)
                toolbar.deleteLater()


    def _createSpineVisualizer(self):
        '''
        '''
        self._clearToolBar()


    def _createNearestNeighborsToolBar(self):
        '''
        '''
        self._clearToolBar()


    def _createDBSCANClustersToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar()
        
        epsilonLabel = QLabel("Epsilon ")
        epsilonField = QLineEdit()
        epsilonField.setMaxLength(10)
        epsilonField.setPlaceholderText("0.5")
        epsilonField.setStatusTip("Epsilon")
        epsilonLabel.setBuddy(epsilonField)

        minPTSLabel = QLabel("Min Points ")
        minPTSField = QLineEdit()
        minPTSField.setMaxLength(10)
        minPTSField.setPlaceholderText("2")
        minPTSField.setStatusTip("Minimum Points")
        minPTSLabel.setBuddy(minPTSField)
        
        # add widgets to the toolbar
        toolBar.addWidget(epsilonLabel)
        toolBar.addWidget(epsilonField)

        toolBar.addWidget(minPTSLabel)
        toolBar.addWidget(minPTSField)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)


    def _createRipleyKFunctionToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar()

        radiusLowBoundLabel = QLabel("Radius Low Limit")
        radiusLowBoundField = QLineEdit()
        radiusLowBoundField.setMaxLength(10)
        radiusLowBoundField.setPlaceholderText("0.01")
        radiusLowBoundField.setStatusTip("Radius lower limit for Ripley K-Function Analysis")
        radiusLowBoundLabel.setBuddy(radiusLowBoundField)

        radiusHighBoundLabel = QLabel("Radius Upper Limit")
        radiusHighBoundField = QLineEdit()
        radiusHighBoundField.setMaxLength(10)
        radiusHighBoundField.setPlaceholderText("100")
        radiusHighBoundField.setStatusTip("Radius upper limit for Ripley K-Function Analysis")
        radiusHighBoundLabel.setBuddy(radiusHighBoundField)

        radiusDensityLabel = QLabel("Radius Array Density")
        radiusDensityField = QLineEdit()
        radiusDensityField.setMaxLength(10)
        radiusDensityField.setPlaceholderText("1000")
        radiusDensityField.setStatusTip("Radius array density for Ripley K-Function Analysis")
        radiusDensityLabel.setBuddy(radiusDensityField)

        # add widgets to the toolbar
        toolBar.addWidget(radiusLowBoundLabel)
        toolBar.addWidget(radiusLowBoundField)

        toolBar.addWidget(radiusHighBoundLabel)
        toolBar.addWidget(radiusHighBoundField)

        toolBar.addWidget(radiusDensityLabel)
        toolBar.addWidget(radiusDensityField)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)


    def _createKenelDensityEstimateToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar()

        bandwidthLabel = QLabel("Bandwidth")
        bandwidthField = QLineEdit()
        bandwidthField.setMaxLength(10)
        bandwidthField.setPlaceholderText("0.1")
        bandwidthField.setStatusTip("Kernel width for density estimation (percentage)")
        bandwidthLabel.setBuddy(bandwidthField)

        evalBuffLabel = QLabel("Eval Buffer")
        evalBuffField = QLineEdit()
        evalBuffField.setMaxLength(10)
        evalBuffField.setPlaceholderText("5")
        evalBuffField.setStatusTip("Evaluation buffer for convolution operation")
        evalBuffLabel.setBuddy(evalBuffField)

        evalSFLabel = QLabel("Eval Scale Factor")
        evalSFField = QLineEdit()
        evalSFField.setMaxLength(10)
        evalSFField.setPlaceholderText("10.0")
        evalSFField.setStatusTip("Evaluation grid multiplicative factor")
        evalSFLabel.setBuddy(evalSFField)

        # add widgets to the toolbar
        toolBar.addWidget(bandwidthLabel)
        toolBar.addWidget(bandwidthField)

        toolBar.addWidget(evalBuffLabel)
        toolBar.addWidget(evalBuffField)

        toolBar.addWidget(evalSFLabel)
        toolBar.addWidget(evalSFField)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)