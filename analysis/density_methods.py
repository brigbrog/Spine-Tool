# Brian Brogan
# Bloss Lab
# The Jackson Laboratory
# 9 November 2026 
# parse script for neuron studio output file
# converts tabular text file to csv


import sys
import numpy as np


from sklearn.cluster import DBSCAN

class SpineDensity:

    @staticmethod
    def get_nn_1D(item, arr):
        '''
         Get Nearest Neighbor
            usage:
            item = current entry in arr to find nearest neighbor index
            arr = array of locations (spine location, 1D) to compare to item
        '''
        dist_arr = arr - item
        abs_dist_arr = np.abs(dist_arr[dist_arr != 0.0])
        min_abs_idx = np.argmin(abs_dist_arr)

        # return min_abs_idx, abs_dist_arr[min_abs_idx]
        return min_abs_idx, abs_dist_arr

    @staticmethod
    def avg_nn_1D(arr):
        '''
        Average Nearest Neighbors for items in <arr>
        '''
        sum_nn_dist = []
        for item in arr:
            nn_idx, nn_dist_arr = SpineDensity.get_nn_1D(item, arr)
            nn_dist = nn_dist_arr[nn_idx]
            sum_nn_dist.append(nn_dist)

        return sum(sum_nn_dist) / len(sum_nn_dist)

    @staticmethod
    def get_nn_nD(item, arr):
        '''
        Get Nearest Neighbor in N Dimensions
        '''
        pass

    @staticmethod
    def avg_nn_nD(arr):
        '''
        Average Nearest Neighbors for items in <arr> (N Dimensions)
        '''
        pass
    

    @staticmethod
    def dbscan(arr, eps, min_pts):
        '''
        Cluster using Density-Based Spatial Clustering of Applications with Noise
        (DBSCAN)
            usage:
             eps = (epsilon) The maximum distance between two objects to be considered neighbors.
             min_pts = (minimum points) The minimum number of points within eps to determine "core point" (cluster)
        '''
        copy = arr.copy()
        if copy.ndim == 1:
            copy = copy.reshape(-1, 1)

        db = DBSCAN(eps=eps, min_samples=min_pts)
        db.fit(copy)

        return db.labels_


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