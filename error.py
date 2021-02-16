#!/usr/bin/env python

import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from utils import read_pose_graph
from scipy.spatial import procrustes
from scipy.linalg import orthogonal_procrustes


"""example
python error.py ../gt_icl_living_traj0/groundtruth.txt ../results_dso_500_images/result.txt dso
python error.py ../gt_icl_living_traj0/groundtruth.txt ../results_dsop_500_images/result.txt dsop

"""

"""some configuration variables"""

plot_aligned_arrays = False
plot_configuration = '3d'
trial_method = ''



def associate_pose_graphs(pose_graph1, pose_graph2):
    """associate pose_graph1 to pose_graph2 according to frame_id, which are the first colomn

    Args:
        pose_graph1 (pandas dataframe): 
            frame_id    x    y    z    qx    qy    qz    qw
        pose_graph2 (pandas dataframe): 
            frame_id    x    y    z    qx    qy    qz    qw

    Returns:
        associated_pose_graph1 (pandas dataframe): a sub graph of pose_graph1
    """

    associated_pose_graph1 = pose_graph1.loc[pose_graph1['frame_id'].isin(pose_graph2['frame_id']).tolist()]

    return associated_pose_graph1

def plot_aligned_array_together(position_array1, position_array2, filename, options = '3d'):
    """[summary]

    Args:
        position_array1 (numpy array): dimension: N x 3
        position_array2 (numpy array): dimension: N x 3
    """
    fig, ax = plt.subplots()
    if options is '3d':
        ax = plt.axes(projection='3d')
        ax.plot3D(position_array1[:,0], position_array1[:,1], position_array1[:,2], 'gray')
        ax.plot3D(position_array1[0:20,0], position_array1[0:20,1], position_array1[0:20,2], 'green')
        ax.plot3D(position_array2[:,0], position_array2[:,1], position_array2[:,2], 'red')
        ax.plot3D(position_array2[0:20,0], position_array2[0:20,1], position_array2[0:20,2], 'green')
        plt.savefig(filename)
        plt.show()
    elif options is '2d':
        plt.plot(position_array1[:,0], position_array1[:,1], 'g')
        plt.plot(position_array2[:,0], position_array2[:,1], 'r')
        plt.plot(position_array1[95::, 0], position_array1[95::, 1], 'g*')
        plt.plot(position_array2[95::, 0], position_array2[95::, 1], 'r*')
        plt.axis('equal')
        plt.savefig(filename)
        plt.show()


def align_sim3(position_array1, position_array2):
    """align the position_array2 to position_array1, to get their differences in SIM(3) parameterization
        algorithm based on DSO evaluation script in MATLAB

    Args:
        position_array1 (numpy array): datatype of numpy array is used to access SVD
                                dimension: N x 3

        position_array2 (numpy array): datatype of numpy array is used to access SVD
                            dimension: N x 3
    Returns:
        scale, translation, rotation, rmse
    """
    print(position_array1.shape)
    print(position_array2.shape)

    if plot_aligned_arrays is True:

        plot_aligned_array_together(position_array1, position_array2, trial_method+'_raw', plot_configuration)

    centroid1 = position_array1.mean(axis=0).reshape(1,3)
    centroid2 = position_array2.mean(axis=0).reshape(1,3)

    H = ((position_array2 - centroid2).transpose()).dot(position_array1 - centroid1)
    U, sdiag, VT = np.linalg.svd(H)
    S = np.zeros((H.shape[0], H.shape[1]))
    np.fill_diagonal(S, sdiag)
    V = VT.transpose()
    R = V.dot(U.transpose())
    if np.linalg.det(R) < 0.0:
        print('determinant negative: ', np.linalg.det(R))
        # V[:,2] = V[:,2] * -1
        # R = V.dot(U.transpose())

    # R, sca = orthogonal_procrustes((position_array2 - centroid2), (position_array1 - centroid1))
    aligned_position_array2 = (position_array2 - centroid2).dot(R.transpose())
    aligned_position_array1 = position_array1 - centroid1

    # print('array shape: ', aligned_position_array1.shape)
    # aligned_position_array1, aligned_position_array2, diff = procrustes(position_array1, position_array2)

    if plot_aligned_arrays is True:
        plot_aligned_array_together(aligned_position_array1, aligned_position_array2, trial_method + '_after_align', plot_configuration)

    # scale1 = (aligned_position_array1**2).sum();
    # scale2 = aligned_position_array1.dot(aligned_position_array2.transpose()).diagonal().sum();

    scale1 = (aligned_position_array2.dot(aligned_position_array1.transpose())).diagonal().sum()
    scale2 = (aligned_position_array2**2).sum();

    scale = abs(scale1/scale2)

    translation = (centroid1.transpose() - scale * R.dot(centroid2.transpose())).transpose()

    rmse = np.sqrt((((scale * aligned_position_array2 - aligned_position_array1)**2).sum(axis=0)/position_array1.shape[0]).sum())

    if plot_aligned_arrays is True:
        plot_aligned_array_together(aligned_position_array1, scale * aligned_position_array2,  trial_method + '_after_align_scale', plot_configuration)

    if np.isnan(scale):
        return np.nan, np.nan, np.nan, np.nan

    return scale, translation, R, rmse



if __name__ == "__main__":



    pose_graph_1 =sys.argv[1]
    pose_graph_2 =sys.argv[2]
    reverse = sys.argv[3] # 0 for forward, 1 for backward
    trial_method = sys.argv[4]


    pg1 = read_pose_graph(pose_graph_1)
    pg2 = read_pose_graph(pose_graph_2)

    
    associated_pg1 = associate_pose_graphs(pg1, pg2)
    # with pd.option_context('display.precision', 15):
    #     print(pg1)
    #     print(pg2)
    #     print(associated_pg1)

    pg2 = pg2.loc[pg2['frame_id'].isin(associated_pg1['frame_id']).tolist()]


    if int(reverse) == 1:
        pg2 = pg2[::-1].reset_index()
    
    
    end_index = associated_pg1.shape[0]
    if len(sys.argv) >5:
        end_index = int(sys.argv[5])

    gt_nparray = associated_pg1[['x', 'y', 'z']].to_numpy()[0:end_index, :]
    pg2_nparray = pg2[['x', 'y', 'z']].to_numpy()[0:end_index, :]
    scale, translation, rotation, rmse = align_sim3(gt_nparray, pg2_nparray)

    print('scale: ' , scale)
    print('translation: ', type(translation), ' ', translation)
    print('rotation: ', type(rotation), ' ', rotation)
    print('rmse: ', type(rmse), ' ', rmse)


    # plot_results()
    