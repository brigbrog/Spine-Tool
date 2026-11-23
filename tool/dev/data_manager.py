# Data Manager 

import sys
import os
import io

import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.stats import gaussian_kde

from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QImage


# add DENSITY METHODS

class DataManager:
    # Data Manager (backend) for spine tool
    def __init__(self, appManager):
        self.appManager = appManager
        self.data = None
        print("data manager initialized")


    def _unloadData(self):
        if isinstance(self.data, pd.DataFrame):
            self.data = None


    def _initData(self, fpath):
        '''
        '''
        file_count = 0
        if (isinstance(fpath, str)) and (os.path.isdir(fpath)):
            for idx, file in enumerate(os.listdir(fpath)):
                file_count += 1
                if file.endswith(".csv"):
                    temp = pd.read_csv(os.path.join(fpath, file))
                    temp['origin'] = file.split(".")[0]
                elif not file.endswith(".csv"):
                    print(f"skipping {file} -> must be CSV format")
                    continue
                if self.data is None:
                    self.data = temp
                else:
                    self.data = pd.concat([self.data, temp])
                del temp
            if self.data is None:
                raise ValueError(f"Provided FPATH {fpath} contains no CSV files")
        else:
            # CATCH THIS WHEN CALLING
            raise ValueError(f"Provided FPATH <{type(fpath)}> is invalid")
        
        self.appManager.statusBar().showMessage(f"Loaded {file_count} files with full shape {self.data.shape}")
        return file_count


    def _cleanBranchData(self):
        '''
        '''
        if self.data is not None:
            if "BRANCH-ORDER" in self.data.columns.tolist():
                self.data["BRANCH-ORDER"] = self.data["BRANCH-ORDER"].fillna(0)
                self.data["BRANCH-ORDER"] = self.data["BRANCH-ORDER"].astype(np.int64)
            else:
                raise ValueError("BRANCH-ORDER not in data columns")
        else:
            raise ValueError("Data has not been initialized")


    def _convertPlot2Array(self, fig):
        '''
        convert a plt.plot to an image array for plotting in the central widget
        '''
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=400) # <---- CREATE DYNAMIC RESOLUTION HELPER
        buf.seek(0)

        image = np.array(Image.open(buf))
        buf.close()

        return image


    def _runAnalysis(self, analysisType):
        '''
        '''
        if analysisType == 'dbscan':
            self._runDBSCAN()
        elif analysisType == 'ripley':
            self._runRIPLEY()
        elif analysisType == 'kde':
            self._runKDE()
        else:
            print("void analysis")


    def _plotAnalysis(self, analysisType):
        '''
        '''
        if self.data is None:
            raise AssertionError("Initialize Data before attempting to plot spine locations")
        assert self.data.shape[0] > 0, "Initialize Data before attempting to plot spine locations"
        if analysisType == 'loc':
            plot = self._plotLOC(0, 0, 500)
        elif analysisType == 'dbscan':
            plot = self._plotDBSCAN()
        elif analysisType == 'ripley':
            plot = self._plotRIPLEY()
        elif analysisType == 'kde':
            plot = self._plotKDE()
        else:
            print("void analysis")
            return

        plotArr = self._convertPlot2Array(plot)
        return plotArr


# RUNNING

    def _runDBSCAN(self):
        print(f' I am DBSCAN')
        pass


    def _runRIPLEY(self):
        print(f' I am RIPLEY')
        pass


    def _runKDE(self):
        print(f' I am KDE')
        pass


# PLOTTING 

    def _plotDBSCAN(self):
        pass

    def _plotRIPLEY(self):
        pass

    def _plotKDE(self):
        pass


    def _plotLOC(self, width, height, size_scale):
        '''
        HEIGHT AND ASPECT SHOULD BE DYNAMIC TO VIEWPORT SIZE
        '''
        g = sns.FacetGrid(self.data, row='origin', height= 2.5, aspect=5, sharex=False, sharey=False, despine=False)
        def plot_spines(data, size_scale, **kwargs):
            ax = plt.gca()
            x = data['SOMA-DISTANCE'].to_numpy()
            y = data['BRANCH-ORDER'].to_numpy()
            s = data['RAYBURST-VOLUME'].to_numpy() * size_scale

            # origin_label = self.data['origin'].iloc[0]
            branch_label = data["BRANCH-ORDER"].iloc[0]

            ax.axhline(y=0, color='r', linestyle='--', linewidth=3.0, alpha=0.2)
            ax.scatter(0, 0, marker='o', color='g', s=75, zorder=2)

            for i, branch in enumerate(data["BRANCH-ORDER"].unique()):
                mask = data["BRANCH-ORDER"] == branch
                x_branch = x[mask]
                y_branch = y[mask]
                s_branch = s[mask]
                ax.scatter(x_branch, y_branch, marker='h', s=s_branch, alpha=0.5, zorder=3, label=f'Branch {i}')

            ax.set_ylim(-0.25, np.max(y) + 2)
            ax.set_yticks([])
            ax.set_ylabel('BRANCH')
            ax.grid(True)

        g.map_dataframe(plot_spines, size_scale=size_scale, hue='BRANCH-ORDER')
        g.set_titles(row_template="{row_name}")

        for ax in g.axes.flat:
            ax.legend(loc="upper right")

        g.figure.suptitle("Spine Locations", x=g.axes.flat[0].get_position().x0, fontsize=16, fontweight='bold', ha='left')
        g.figure.tight_layout(rect=[0, 0, 1, 1])

        return g




# STATIC METHODS

    @staticmethod
    def _ndarray2QImage(image: np.ndarray):
      qimage = QImage(image.data, 
                      image.shape[1],
                      image.shape[0],
                      image.strides[0],
                      QImage.Format.Format_RGBA8888)

      return qimage


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

        return sum(sum_nn_dist) / len(sum_nn_dist), sum_nn_dist


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
    def gaussian_kde_1D(arr, bandwidth='scott', eval_buff=2, eval_sf=1.0):
        '''
        Gaussian Kernel Density Estimate (KDE)
            (convolves input array with gaussian kernel)

            if eval_sf (evalutaion size factor) = 'same', then the kernel is estimated on a vector with the same shape
                as the input array. Otherwise the estimate size is controlled by int eval_size
        '''
        eval_size = round(eval_sf * np.max(arr))
        gauss_kde = gaussian_kde(arr, bw_method=bandwidth)
        eval_grid = np.linspace(np.min(arr) - eval_buff, np.max(arr) + eval_buff, eval_size)

        return eval_grid, gauss_kde(eval_grid)


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
    def vmr(arr):
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

        return counts_vmr, counts, bin_edges


    @staticmethod
    def ripley_kfunc_1D(arr, L, r):
        '''
        L : Length of domain (section-length)
        r : radius
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
