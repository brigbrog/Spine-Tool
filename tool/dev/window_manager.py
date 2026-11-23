# Window Manager 

import sys
import os
from pathlib import Path

import numpy as np
from PIL import Image

import seaborn as sns
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout
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
    # Window Manager (frontend) for SpineToolApp
    def __init__(self, appManager):
        
        self.appManager = appManager
        self._initUI()


    def _initUI(self):
        '''
        Intialize the window userface
        '''
        self.appManager.graphicsView = QGraphicsView(self.appManager)
        self.appManager.graphicsView.setFrameShape(QFrame.Shape.NoFrame)
        self.appManager.graphicsView.setViewportMargins(10, 10, 10, 10)

        # self.appManager.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.appManager.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
                        "Hide the analysis ToolBar"
                    ),
                    None,  # separator
                    ("&Exit", self.appManager.close, "Ctrl+Q", "Close Spine Tool"), # <- handle this signal for confirmation
                    None,
                    ("&Load Test Image", self.appManager._loadTestImage, "", ""),
                    ("&Clear Viewport", self.appManager._clearViewPort, "", ""),
                ],
            ),
            (
                "&Analyze",
                [
                    ("Spine Visualizer", self._createSpineVisualizerToolBar, None, "Open Spine Visualizer"), 
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

    # TOOL BARS

    def _createRunButton(self, analysisType: str):
        '''
        '''
        runButton = QPushButton("Run")
        # runButton.clicked.connect(self.appManager._runAnalysis(analysisType))
        runButton.clicked.connect(lambda _checked=False, kind=analysisType: self.appManager._runAnalysis(kind))

        return runButton

    def _createPlotButton(self, analysisType: str):
        '''
        '''
        plotButton = QPushButton("Plot")
        plotButton.clicked.connect(lambda _checked=False, kind=analysisType: self.appManager._plotAnalysis(kind))

        return plotButton

    def _clearToolBar(self):
        '''
        '''
        for toolbar in self.appManager.findChildren(QToolBar):
            if self.appManager.toolBarArea(toolbar) == Qt.ToolBarArea.RightToolBarArea:
                self.appManager.removeToolBar(toolbar)
                toolbar.deleteLater()

    def _createSpineVisualizerToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar()

        title = QLabel("Spine Locations")

        # PLOT
        plotButton = self._createPlotButton("loc")

        # add widgets to the toolbar
        toolBar.addWidget(title)
        toolBar.addWidget(plotButton)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)


    def _createNearestNeighborsToolBar(self):
        '''
        '''
        self._clearToolBar()


    def _createDBSCANClustersToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar()
        
        title = QLabel("DBSCAN")

        # EPS
        epsilonLabel = QLabel("Epsilon ")
        epsilonField = QLineEdit()
        epsilonField.setMaxLength(10)
        epsilonField.setPlaceholderText("0.5")
        epsilonField.setStatusTip("Epsilon")
        epsilonLabel.setBuddy(epsilonField)

        # MIN PTS
        minPTSLabel = QLabel("Min Points ")
        minPTSField = QLineEdit()
        minPTSField.setMaxLength(10)
        minPTSField.setPlaceholderText("2")
        minPTSField.setStatusTip("Minimum Points")
        minPTSLabel.setBuddy(minPTSField)

        # RUN / PLOT
        runButton = self._createRunButton("dbscan")
        plotButton = self._createPlotButton("dbscan")
        
        # add widgets to the toolbar
        toolBar.addWidget(title)
        
        toolBar.addWidget(epsilonLabel)
        toolBar.addWidget(epsilonField)

        toolBar.addWidget(minPTSLabel)
        toolBar.addWidget(minPTSField)

        toolBar.addWidget(runButton)
        toolBar.addWidget(plotButton)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)


    def _createRipleyKFunctionToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar()

        title = QLabel("Ripley K-Function")

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

        # RUN / PLOT
        runButton = self._createRunButton("ripley")
        plotButton = self._createPlotButton("ripley")

        # add widgets to the toolbar
        toolBar.addWidget(title)

        toolBar.addWidget(radiusLowBoundLabel)
        toolBar.addWidget(radiusLowBoundField)

        toolBar.addWidget(radiusHighBoundLabel)
        toolBar.addWidget(radiusHighBoundField)

        toolBar.addWidget(radiusDensityLabel)
        toolBar.addWidget(radiusDensityField)

        toolBar.addWidget(runButton)
        toolBar.addWidget(plotButton)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)


    def _createKenelDensityEstimateToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar()

        title = QLabel("Kernel Density Estimate")

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

        # RUN / PLOT
        runButton = self._createRunButton("kde")
        plotButton = self._createPlotButton("kde")

        # add widgets to the toolbar
        toolBar.addWidget(title)

        toolBar.addWidget(bandwidthLabel)
        toolBar.addWidget(bandwidthField)

        toolBar.addWidget(evalBuffLabel)
        toolBar.addWidget(evalBuffField)

        toolBar.addWidget(evalSFLabel)
        toolBar.addWidget(evalSFField)

        toolBar.addWidget(runButton)
        toolBar.addWidget(plotButton)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)