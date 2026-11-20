# Data Manager 

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

from layout_objects import ImageWindow

class DataManager:
    # DataManager class (backend) for spine tool
    def __init__(self, appManager):
        self.appManager = appManager
        print("data manager initialized")

    def _scramble(self, image):
        img_hc, img_wc = self._getImageCenter(image)
        new_image = np.random.uniform(low=0.0, high=255.0, size = image.shape)
        return new_image

    def _getImageCenter(self, arr: np.ndarray):
        height, width, _ = arr.shape
        return float(height // 2), float(width // 2)

    # def _getImageDataFromViewer(self):
    #     '''
    #     Pulls data from the scene <GraphicsView> and converts it to a QImage

    #     Params:
    #         None
    #     Returns:
    #         <QImage> of the data present in the scene GraphicsView
    #     '''
    #     # search for pixmap items in the scene
    #     pixmap_item = None
    #     for item in self.scene.items():
    #         if isinstance(item, QGraphicsPixmapItem):
    #             pixmap_item = item
    #             break
    #     # if no pixmap item was found in the scene, return None
    #     if not pixmap_item:
    #         return None

    #     # convert the pixmap item to a QImage
    #     pixmap = pixmap_item.pixmap()
    #     qimage = pixmap.toImage()

    #     return qimage

    def _qImage2Pil(self, qImage: QImage):
        '''
        Converts a <QImage> to a pillow <Image>

        Params:
            <QImage> Any
        Returns:
            <Image> pillow image 
        '''
        if qImage is not None:
            arr = self._qImage2Ndarray(qImage)
            pilImage = Image.fromarray(arr)

            return pilImage

    def _pil2QImage(self, pilImage: Image):
        '''
        Converts numpy <ndarray> to PyQt <QImage>

        Params:
            <Image> pillow <Image>
        Returns:
            <QImage> format (RGBA8888)
        '''
        arr = np.asarray(pilImage)
        qImage = self._ndarray2QImage(arr)
        return qImage

    def _qImage2Ndarray(self, qImage: QImage):
        '''
        Converts a <QImage> to a numpy <ndarray>

        Params:
            <QImage> Any
        Returns:
            <ndarray> numpy array in image format (RGBA8888)
        '''
        if qImage is not None:
            qImage = qImage.convertToFormat(QImage.Format.Format_RGBA8888)
            width = qImage.width()
            height = qImage.height()

            ptr = qImage.bits()
            ptr.setsize(qImage.sizeInBytes())
            arr = np.array(ptr).reshape((height, width, 4))

            return arr

    def _ndarray2QImage(self, image: np.ndarray):
        '''
        Converts numpy <ndarray> to PyQt <QImage>

        Params:
            <ndarray> array in image format (Y, X, RGBA)
        Returns:
            <QImage> format (RGBA8888)
        '''
        qImage = QImage(image.data, 
                        image.shape[1],
                        image.shape[0],
                        image.strides[0],
                        QImage.Format.Format_RGBA8888)

        return qImage