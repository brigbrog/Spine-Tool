# Brian Brogan
# Bloss Lab
# The Jackson Laboratory
# 11 November 2026


# KS test maybe somewhere else

from kernel_generation import KernelGen

import sys
import numpy as np


from sklearn.cluster import DBSCAN
from scipy.stats import gaussian_kde

class SpineDensity:

    @staticmethod
    def get_nn_1D(item, arr, drop_self = True):
        '''
         Get Nearest Neighbor
            usage:
            item = current entry in arr to find nearest neighbor index
            arr = array of locations (spine location, 1D) to compare to item
        '''
        dist_arr = arr - item
        if drop_self:
            abs_dist_arr = np.abs(dist_arr[dist_arr != 0.0])
        else:
            abs_dist_arr = np.abs(dist_arr)
        if len(abs_dist_arr) == 0:
            return None, None
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
    def gaussian_kde_1D(arr, bandwith, eval_buff=2, eval_size='same'):
        '''
        Gaussian Kernel Density Estimate (KDE)
            (convolves input array with gaussian kernel)

            if eval_size = 'same', then the kernel is estimated on a vector with the same shape
                as the input array. Otherwise the estimate size is controlled by int eval_size
        '''
        if eval_size == 'same':
            #eval_size = arr.shape[0]
            eval_size = np.max(arr)
        gauss_kde = gaussian_kde(arr)
        eval_grid = np.linspace(np.min(arr) - eval_buff, np.max(arr) + eval_buff, eval_size)

        return gauss_kde(eval_grid)


    # ADD support for kernel customization
    @staticmethod
    def kde_1D(arr, kernel_type, eval_buff_p, eval_size, **kwargs):
        '''
        '''

        if kernel_type == 'gauss':
            kernel = KernelGen.gauss1D(**kwargs)

        # apply convolution for kernel density estimate

        return


    @staticmethod
    def vmr(arr);
        '''
        Variance to mean ratio
            VMR = 1 -> consistent with poisson
            VMR < 1 -> more uniform than random 
            VMR > 1 -> less uniform than random (clustered)
            VMR = 0 -> constant
        '''
        var = np.var(arr)
        mean = np.mean(arr)

        if mean == 0:
            raise ValueError("<arr> has null mean")

        return var**2/mean


    @staticmethod
    def dispersion_index(arr, num_bins):
        '''
        Dispersion Index
            bin-based vmr analysis for spine locations
            calculates vmr of binned spine data.
        '''
        counts, bin_edges = np.histogram(arr, bins=num_bins)
        if len(counts) <= 1 or np.all(counts == 0):
            raise ValueError("bins result is incompatible")

        counts_vmr = SpineDensity.vmr(counts)

        return, counts_vmr, counts, bin_edges


    @staticmethod
    def ripley_kfunc_1D(arr, L, r):
        '''
        '''

        n = arr.shape[0]
        if n <= 1:
            raise ValueError("<arr> is too short")
        k_sum = 0.0

        for item in arr:
            min_abs_idx, abs_dist_arr = SpineDensity.get_nn_1D(item, arr, drop_self=False)
            r_mask = (abs_dist_arr > 0.0) & (abs_dist_arr <= r)
            r_neighbors = arr[r_mask]

            if len(r_neighbors) == 0:
                continue

            # edge correction
            window_start = max(0.0, item - r)
            window_end = min(L, item + r)
            length = window_end - window_start
            full_length = 2.0 * r

            # calculate correction factor
            c = full_length / length if length > 0 else 1.0

            # increment the sum
            k_sum += len(r_neighbors) * c 
        
        return (L * k_sum) / (n * (n - 1))


    @staticmethods
    def lin_1d_lfunc():
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