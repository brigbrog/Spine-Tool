# Data Manager 

import sys
import os
import io

# sys.path.append("../../analysis")

from density_methods import SpineDensity as sd

import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.stats import gaussian_kde

from PyQt6.QtGui import QImage # QAction, QIcon, QKeySequence, QPixmap,


class DataManager:
    # Data Manager (backend) for spine tool
    def __init__(self, appManager):
        self.appManager = appManager
        self.data = None

        self.nnData = None
        self.dbscanData = None
        self.ripleyData = None 
        self.kdeData = None

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


# CONTROL


    def _runAnalysis(self, analysisType, analysisParams: dict):
        '''
        '''
        if self.data is None:
            raise AssertionError("Initialize Data before attempting to analyze")
        assert self.data.shape[0] > 0, "Initialize Data before attempting to plot"

        if analysisType == 'nn':
            self.nnData = self._runNN() # TAKES NO PARAMS
        elif analysisType == 'dbscan':
            self.dbscanData = self._runDBSCAN(**analysisParams)
        elif analysisType == 'ripley':
            self.ripleyData = self._runRIPLEY(**analysisParams)
        elif analysisType == 'kde':
            self.kdeData = self._runKDE(**analysisParams)
        else:
            print("void analysis")


    def _plotAnalysis(self, analysisType):
        '''
        '''
        if self.data is None:
            raise AssertionError("Initialize Data before attempting to plot")
        assert self.data.shape[0] > 0, "Initialize Data before attempting to plot"

        if analysisType == 'loc':
            plot = self._plotLOC(500)
        elif analysisType == 'nn':
            #self.nnData = self._runNN()
            if self.nnData is None:
                # self.appManager.statusBar().showMessage("RUN ANALYSIS BEFORE PLOTTING")
                return
            plot = self._plotNN(self.nnData)
        elif analysisType == 'dbscan':
            if self.dbscanData is None:
                # self.appManager.statusBar().showMessage("RUN ANALYSIS BEFORE PLOTTING")
                return
            plot = self._plotDBSCAN(self.dbscanData)
        elif analysisType == 'ripley':
            if self.ripleyData is None:
                # self.appManager.statusBar().showMessage("RUN ANALYSIS BEFORE PLOTTING")
                return
            plot = self._plotRIPLEY(self.ripleyData)
        elif analysisType == 'kde':
            if self.kdeData is None:
                # self.appManager.statusBar().showMessage("RUN ANALYSIS BEFORE PLOTTING")
                return
            plot = self._plotKDE(self.kdeData)
        else:
            print("void analysis")
            return

        plotArr = self._convertPlot2Array(plot)
        return plotArr


# RUN ANALYSIS


    def _runNN(self):
        '''
        '''
        nn_dfs = [] 
        for idx, origin in enumerate(self.data['origin'].unique().tolist()):
            spines_i = self.data.loc[self.data['origin'] == origin, 'SOMA-DISTANCE'].to_numpy()
            branch_i = self.data.loc[self.data['origin'] == origin, 'BRANCH-ORDER'].to_numpy()
            avg_nn_spines, dist_arr = sd.avg_nn_1D(spines_i)
            df_origin = pd.DataFrame({
                    'origin': origin,
                    'branch': branch_i,
                    'branch_str': f'Branch {branch_i}',
                    'nn_dist': dist_arr,
                    'avg_nn': avg_nn_spines  # Optional: repeats the group mean on each row if needed
            })
            nn_dfs.append(df_origin)

        nn_df = pd.concat(nn_dfs, ignore_index=True)
        nn_df['branch_str'] = nn_df['branch'].map({i : f'Branch {i}' for i in nn_df['branch'].unique()})

        return nn_df


    def _runDBSCAN(self, eps=0.5, min_pts=2): 
        '''
        '''
        scan_dfs = []
        for idx, origin in enumerate(self.data['origin'].unique().tolist()):
            for branch in np.unique(self.data[self.data['origin'] == origin]['BRANCH-ORDER'].unique()):
                branch_mask = (self.data['origin'] == origin) & (self.data['BRANCH-ORDER'] == branch)
                branch_scan = sd.dbscan(self.data[branch_mask].loc[:, 'SOMA-DISTANCE'].to_numpy(), eps, min_pts)

                branch_df = pd.DataFrame({
                    'origin' : origin,
                    'branch' : branch,
                    'spine_arr' : self.data[branch_mask].loc[:, 'SOMA-DISTANCE'].to_numpy(),
                    'clust_arr' : branch_scan,
                    'c2p_ratio' : np.unique(branch_scan).shape[0] / self.data[branch_mask].shape[0]
                    })
                scan_dfs.append(branch_df)
        scans_df = pd.concat(scan_dfs, ignore_index=True)

        return scans_df


    def _runRIPLEY(self, low=1e-5, high=25, density=100):
        '''
        '''
        rad_arr = np.linspace(low, high, density)
        csr = 2.0 * rad_arr

        rip_dfs = []
        for idx, origin in enumerate(self.data['origin'].unique().tolist()):
            for branch in np.unique(self.data[self.data['origin'] == origin]['BRANCH-ORDER'].unique()):
                branch_mask = (self.data['origin'] == origin) & (self.data['BRANCH-ORDER'] == branch)
                spine_i = self.data[branch_mask].loc[:, 'SOMA-DISTANCE'].to_numpy()
                L = self.data[branch_mask].loc[0, 'SECTION-LENGTH']
                rip_arr = np.array([sd.ripley_kfunc_1D(spine_i, L, r) for r in rad_arr])

                branch_df = pd.DataFrame({
                    'origin' : origin,
                    'branch' : branch,
                    'rad_arr' : rad_arr,
                    'rip_arr' : rip_arr,
                    'rip_diff_arr' : rip_arr - csr,
                    'csr' : csr
                })
                rip_dfs.append(branch_df)
        rip_df = pd.concat(rip_dfs, ignore_index=True)

        return rip_df


    def _runKDE(self, bandwidth=0.1, eval_buff=1, eval_sf=10.0):
        '''
        '''
        kde_dfs = []

        for idx, origin in enumerate (self.data['origin'].unique().tolist()):
            for branch in np.unique(self.data[self.data['origin'] == origin]['BRANCH-ORDER'].unique()):
                branch_mask = (self.data['origin'] == origin) & (self.data['BRANCH-ORDER'] == branch)
                spine_i = self.data[branch_mask].loc[:, 'SOMA-DISTANCE'].to_numpy()
                eval_grid, spine_gauss_kde = sd.gaussian_kde_1D(spine_i, bandwidth, eval_buff, eval_sf)

                branch_df = pd.DataFrame({
                    'origin' : origin,
                    'branch' : branch,
                    'kde': spine_gauss_kde, 
                    'eval_grid' : eval_grid
                })
                kde_dfs.append(branch_df)
        kde_df = pd.concat(kde_dfs, ignore_index=True)

        return kde_df


# PLOT ANALYSIS


    def _plotLOC(self, size_scale):
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


    def _plotNN(self, nn_data):
        '''
        '''
        fig = plt.figure(figsize=(15, 5))
        s = sns.stripplot(data=nn_data, x='nn_dist', y='origin', marker='o', jitter=True, alpha=0.5, size=7, orient='h', hue='branch_str')
        b = sns.boxplot(data=nn_data, x='nn_dist', y='origin', width=0.5, showfliers=False, boxprops=dict(facecolor='none', edgecolor='black', linewidth=1.2))

        plt.xlabel("Nearest Neighbors Distances")
        fig.suptitle("Nearest Neighbors", x=0, y=1, fontsize=16, fontweight='bold', ha='left')

        ax = plt.gca()
        ax.yaxis.set_ticks_position('right')
        ax.yaxis.set_label_position('right')
        ax.set_ylabel("")
        plt.tight_layout()

        return fig


    def _plotDBSCAN(self, dbscanData):
        g = sns.FacetGrid(dbscanData, row='origin', aspect=5, height=3, sharex=False, sharey=False, despine=False)
        def y_shift(num_branches):
            return 0.75 * (1 / num_branches)
        def plot_clusters(data, **kwargs):
            ax = plt.gca()

            x = data['spine_arr']
            y = data['clust_arr']

            for i, branch in enumerate(data['branch'].unique()):
                n_branches = data['branch'].unique().size

                mask = data['branch'] == branch
                x_branch = x[mask]
                y_branch = y[mask] + y_shift(n_branches) * i
                ax.scatter(x_branch, y_branch, label=f'Branch {i}', alpha=0.8)

            ax.set_ylim(-1.5, np.max(y_branch) + 2)
            ax.set_yticks([0] + np.arange(-1, np.max(y_branch)+1, 1))
            ax.grid(True)

        g.map_dataframe(plot_clusters, hue='branch')
        g.set_titles(row_template="{row_name}")
        for ax in g.axes.flat:
            ax.legend(loc="upper right")

        g.figure.suptitle(
            "Spine Clusters (DBSCAN)", x=g.axes.flat[0].get_position().x0, fontsize=16, fontweight='bold', ha='left')
        g.figure.tight_layout(rect=[0, 0, 1, 1])

        return g


    def _plotRIPLEY(self, ripleyData):
        '''
        '''
        g = sns.FacetGrid(ripleyData, row='origin', aspect=5, height=3, sharex=True, sharey=False, despine=False)

        def plot_ripleys(data, **kwargs):
            ax = plt.gca()

            # plot Ripley's
            sns.lineplot(data=data, x="rad_arr", y="rip_arr", errorbar="sd", ax=ax, alpha = 0.8, label = 'L(r)')
            sns.lineplot(data=data, x='rad_arr', y='rip_diff_arr', errorbar='sd', ax=ax, alpha = 0.8, label = 'L(r) - r')

            # plot CSR
            sns.lineplot(data=data, x='rad_arr', y='csr', errorbar=None, linestyle = '--', color = 'black', label = 'CSR')
            sns.lineplot(data=data, x='rad_arr', y=np.zeros_like(data['rad_arr']), errorbar=None, linestyle='--', color = 'black')

            ax.set_ylabel('Ripley Value')
            ax.set_xlabel('Radius')
            ax.grid(True)

        g.map_dataframe(plot_ripleys)
        g.set_titles(row_template="{row_name}")
        for ax in g.axes.flat:
            ax.legend(loc="upper right")

        g.figure.suptitle("Ripley's K-Function Analysis", x=g.axes.flat[0].get_position().x0, fontsize=16, fontweight='bold', ha='left')
        g.figure.tight_layout(rect=[0, 0, 1, 1])

        return g


    def _plotKDE(self, kdeData):
        '''
        '''
        g = sns.FacetGrid(kdeData, row='origin', aspect=5, height=3, sharex=False, sharey=False, despine=False)

        def plot_kde(data, **kwargs):
            ax = plt.gca()

            x = data['eval_grid']
            y = data['kde']

            for i, branch in enumerate(data['branch'].unique()):
                mask = data['branch'] == branch

                x_branch = x[mask]
                y_branch = y[mask]
                ax.plot(x_branch, y_branch, alpha=0.5, linewidth=2, label=f'Branch {i}')
                ax.set_ylabel('Density')
                ax.set_xlabel('Spine Location')
                ax.grid(True)

        g.map_dataframe(plot_kde)
        g.set_titles(row_template="{row_name}")
        origins = self.data['origin'].unique()

        for i, ax in enumerate(g.axes.flat):
            spine_mask = (self.data['origin'] == origins[i])
            branches = self.data[spine_mask]['BRANCH-ORDER'].unique()
            ax.legend(loc="upper right")
            for i, branch in enumerate(branches):
                sub_branch = self.data[spine_mask & (self.data['BRANCH-ORDER'] == branch)]['SOMA-DISTANCE']
                ax.scatter(sub_branch, np.full(sub_branch.shape, -1 * 0.005 * i), marker = 'x', s = 50)

        g.figure.suptitle("Gaussian Kernel Density Estimate", x=g.axes.flat[0].get_position().x0, fontsize=16, fontweight='bold', ha='left')
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