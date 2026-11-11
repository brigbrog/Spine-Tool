# Brian Brogan
# Bloss Lab
# The Jackson Laboratory
# 9 November 2026 
# parse script for neuron studio output file
# converts tabular text file to csv


import sys
import numpy as np


class SpineDensity:

    @staticmethod
    def get_nn(item, arr):
        '''
         Get Nearest Neighbor
            usage:
            item = current entry in arr to find nearest neighbor index
            arr = array of locations (spine location, 1D) to compare to item
        '''
        dist_arr = arr - item
        abs_dist_arr = np.abs(dist_arr[dist_arr != 0.0])
        min_abs_idx = np.argmin(abs_dist_arr)

        return min_abs_idx, abs_dist_arr[min_abs_idx]

    @staticmethod
    def avg_nearest_neighbor(arr):
        '''
        Average Nearest Neighbors in <arr>
        '''
        sum_nn_dist = []
        for item in arr:
            _, nn_dist = SpineDensity.get_nn(item, arr)
            sum_nn_dist.append(nn_dist)

        return sum(sum_nn_dist) / len(sum_nn_dist)


    @staticmethod
    def db_scan(eps, min_pts):
        pass

    @staticmethod
    def kernel_density_estimate():
        pass

    @staticmethod
    def dispersion_index():
        pass

    @staticmethod
    def lin_1d_lfunc():
        pass

    @staticmethod
    def ripley_kfunc():
        # account for edge effects
        pass

    @staticmethod
    def coe_var():
        pass

    @staticmethod
    def auc():
        pass

    @staticmethod
    def pearson_cor():
        pass



if __name__ == "__main__":
    data = sys.stdin.read()
    print(data)