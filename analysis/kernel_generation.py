# kernel generator file 


import numpy as np


class KernelGen:

    @staticmethod
    def gauss1D(n, sigma):
        '''
        Generate a N-Dimensional guassian kernel
        '''
        if n % 2 == 0:
            raise ValueError("n must be odd")

        k = n // 2
        x_grid = np.arange(-k, k + 1)

        kernel = np.exp(-(x_grid**2) / (2 * (sigma**2)))

        return kernel / np.sum(kernel)

