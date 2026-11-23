'''
Developed by Brian Brogan
image utilities for KnitKit -------> SUPPORTS ONLY PILLOW, NUMPY DATA
For knitkit run see KnitKitApp.py
November 2026
'''

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from scipy.signal import convolve


class ImageUtil:
    @staticmethod
    def _scramble(self, image):
        img_hc, img_wc = self._getImageCenter(image)
        new_image = np.random.uniform(low=0.0, high=255.0, size = image.shape)
        return new_image

    @staticmethod
    def _getImageCenter(self, arr: np.ndarray):
        height, width, _ = arr.shape
        return float(height // 2), float(width // 2)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
