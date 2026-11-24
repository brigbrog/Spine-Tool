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
from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout, QSlider
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











    # def _parseDBSCANParams(self, epsilonField: QLineEdit, minPTSField: QLineEdit) -> dict:
    #     raw_eps = epsilonField.text().strip()
    #     raw_min_pts = minPTSField.text().strip()

    #     try:
    #         eps = float(raw_eps) if raw_eps else 0.5
    #     except ValueError as exc:
    #         raise ValueError("Epsilon must be a valid number.") from exc

    #     if eps <= 0:
    #         raise ValueError("Epsilon must be greater than 0.")

    #     try:
    #         min_pts = int(raw_min_pts) if raw_min_pts else 2
    #     except ValueError as exc:
    #         raise ValueError("Min Points must be a whole number.") from exc

    #     if min_pts < 1:
    #         raise ValueError("Min Points must be at least 1.")

    #     return {"eps": eps, "min_samples": min_pts}


    # def _parseLineEditFloat(self, field: QLineEdit, default: float, type) -> float:
    #     raw = field.text().strip()
    #     print(f'raw read dbscan : {raw}')
    #     try: 
    #         flt = float(raw) if raw else default
    #     except ValueError as exc:
    #         raise ValueError("Field entry cannot be converted to valid float") from exc
    #     print(f'parsed output : {flt}')
    #     return flt.astype(type)


    # def _parseLineEditValue(self, field: QLineEdit, default, target_type):
        # raw = field.text().strip()
        # print(f'raw read dbscan : {raw}')
        # try:
        #     value = target_type(raw) if raw else default
        # except ValueError as exc:
        #     # value = target_type(default)
        #     value = default
        #     #                                                                                            ADD A STATUS MESSAGE HERE
        # print(f'parsed output : {value}')
        # return value


    def _parseLineEditValue(self, field: QLineEdit, default, target_type):
        '''
        ADD RANGE LIMIT
        '''
        raw = field.text().strip()
        print(f'raw read dbscan : {raw}')
        if not raw:
            value = default
        else:
            try:
                value = target_type(raw)
            except ValueError:
                if target_type is int:
                    try:
                        value = int(float(raw))
                    except ValueError:
                        value = default
                        # ADD A STATUS MESSAGE HERE
                else:
                    value = default
                    # ADD A STATUS MESSAGE HERE
        print(f'parsed output : {value}')
        return value










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
                    ("&Load Test Image", self.appManager._loadTestImage, "Ctrl+T", ""),
                    ("&Clear Viewport", self.appManager._clearViewPort, "Ctrl+C", ""),
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

    # def _createRunButton(self, analysisType: str, analysisParams: dict):
    # def _createRunButton(self, analysisType: str, fields: dict):
    #     '''
    #     analysisParams {"analysisType": str, "analysisParams": dict}
    #     '''
    #     runButton = QPushButton("Run")

    #     analysisParams = {}
    #     for param, (field, default) in fields.items():
    #         analysisParams[param] = self._parseLineEditFloat(field, default)

    #     toPass = {
    #     'analysisType': analysisType,
    #     'analysisParams': analysisParams
    #     }
    #     runButton.clicked.connect(lambda _checked=False, kind=toPass: self.appManager._runAnalysis(kind))

    #     return runButton


    def _createRunButton(self, analysisType: str, fields: dict):
        '''
        analysisParams {"analysisType": str, "analysisParams": dict}
        '''
        runButton = QPushButton("Run")

        def onClicked(_checked=False):
            analysisParams = {
                # param: self._parseLineEditFloat(field, default, type)
                param: self._parseLineEditValue(field, default, type)
                for param, (field, default, type) in fields.items()
            }
            toPass = {
                "analysisType": analysisType,
                "analysisParams": analysisParams,
            }
            self.appManager._runAnalysis(toPass)

        runButton.clicked.connect(onClicked)
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

        # CONTROLS
        # heightLabel = QLabel("")
        # heightSlider =  QSlider(Qt.Orientation.Horizontal)
        # aspectSlider
        # sizeSlider

        # add widgets to the toolbar
        toolBar.addWidget(title)
        # toolBar.addWidget(heightSlider)
        toolBar.addWidget(plotButton)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)


    def _createNearestNeighborsToolBar(self):
        '''
        '''
        self._clearToolBar()
        toolBar = QToolBar ()

        title = QLabel("Nearest Neighbors")

        # PLOT
        runParams = {}
        runButton = self._createRunButton("nn", runParams)
        plotButton = self._createPlotButton("nn")

        # CONTROLS
        # somethingSlider = QSlider(Qt.Orientation.Horizontal)

        # add widgets to the toolbar
        toolBar.addWidget(title)
        # toolBar.addWidget(somethingSlider)
        toolBar.addWidget(runButton)
        toolBar.addWidget(plotButton)

        self.appManager.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolBar)


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

        # param, (field, default)

        runParams = {
            'eps' : (epsilonField, 0.5, float),
            'min_pts' : (minPTSField, 2, int)
        }

        runButton = self._createRunButton("dbscan", runParams)
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

        runParams = {
            'low' : (radiusLowBoundField, 0.01, float),
            'high' : (radiusHighBoundField, 100, float),
            'density' : (radiusDensityField, 1000, int)
        }

        # RUN / PLOT
        runButton = self._createRunButton("ripley", runParams)
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

        runParams = {
            'bandwidth' : (bandwidthField, 0.1, float),
            'eval_buff' : (evalBuffField, 5, int),
            'eval_sf' : (evalSFField, 10.0, float)
        }

        # RUN / PLOT
        runButton = self._createRunButton("kde", runParams)
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