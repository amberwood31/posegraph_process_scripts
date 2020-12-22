#!/usr/bin/env python

import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


plot_aligned_arrays = True



def read_pose_graph(pose_graph_path):
    """[summary]

    Args:
        pose_graph_path (str): [description]
    
    Returns:
        pose_graph (pandas dataframe): 
            frame_id    x    y    z    qx    qy    qz    qw

    """
    pose_graph = pd.read_csv(pose_graph_path, delim_whitespace=True , header = None, names = ['frame_id', 'x', 'y', 'z', 'qx', 'qy', 'qz', 'qw']) 

    return pose_graph



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

def plot_aligned_array_together(position_array1, position_array2, options = '3d'):
    """[summary]

    Args:
        position_array1 (numpy array): dimension: N x 3
        position_array2 (numpy array): dimension: N x 3
    """
    fig, ax = plt.subplots()
    if options is '3d':
        ax = plt.axes(projection='3d')
        ax.plot3D(position_array1[0], position_array1[1], position_array1[2], 'gray')
        ax.plot3D(position_array2[0], position_array2[1], position_array2[2], 'red')
        plt.show()
    elif options is '2d':
        plt.plot(position_array1[0], position_array1[1], 'g')
        plt.plot(position_array2[0], position_array2[1], 'r')
        plt.axis('equal')
        plt.show()


def align_sim3(position_array1, position_array2):
    """align the two position arrays to get their differences in SIM(3) parameterization
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

    plot_aligned_array_together(position_array1, position_array2, '2d')

    centroid1 = position_array1.mean(axis=0).reshape(1,3)
    centroid2 = position_array2.mean(axis=0).reshape(1,3)

    H = (position_array1 - centroid1).transpose().dot(position_array2 - centroid2)
    U, S, V = np.linalg.svd(H)
    R = V.dot(U.transpose())

    if np.linalg.det(R) < 0.0:
        V[:,2] = V[:,2] * -1
        R = V.dot(U.transpose())

    aligned_position_array2 = (position_array2 - centroid2).dot(R.transpose())
    aligned_position_array1 = position_array1 - centroid1

    if plot_aligned_arrays is True:
        plot_aligned_array_together(aligned_position_array1, aligned_position_array2, '2d')

    scale2 = (aligned_position_array2**2).sum();
    scale1 = aligned_position_array1.dot(aligned_position_array2.transpose()).diagonal().sum();

    scale = scale2/scale1

    translation = (centroid1.transpose() - scale * R.dot(centroid2.transpose())).transpose()

    rmse = np.sqrt(((scale * aligned_position_array2 - aligned_position_array1)**2).sum()/position_array1.shape[0])

    if np.isnan(scale):
        return np.nan, np.nan, np.nan, np.nan

    return scale, translation, R, rmse



if __name__ == "__main__":
    pose_graph_1 =sys.argv[1]
    pose_graph_2 =sys.argv[2]
    

    pg1 = read_pose_graph(pose_graph_1)
    pg2 = read_pose_graph(pose_graph_2)

    
    associated_pg1 = associate_pose_graphs(pg1, pg2)
    # with pd.option_context('display.precision', 15):
    #     print(pg1)
    #     print(pg2)
    #     print(associated_pg1)

    scale, translation, rotation, rmse = align_sim3(associated_pg1[['x', 'y', 'z']].to_numpy(), \
         pg2[['x', 'y', 'z']].to_numpy())

    print('scale: ' , scale)
    print('translation: ', translation)
    print('rotation: ', rotation)
    print('rmse: ', rmse)


    # plot_results()
    