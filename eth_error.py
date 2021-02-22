#!/usr/bin/env python

import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from utils import read_pose_graph, read_timestamp_id, read_pose_graph_with_timestamp
from error import align_sim3, plot_aligned_array_together 
from scipy.spatial import procrustes
from scipy.linalg import orthogonal_procrustes


"""example
python dso_error.py /media/amber/www/data/dso_supp_v2/gtFiles/sim_office_traj0.txt /media/amber/www/data/dso_supp_v2/DS-VO_Forward/sim_office_traj0_6.txt test 100

"""

"""some configuration variables"""

plot_aligned_arrays = False
plot_configuration = '2d'
trial_method = ''



def associate_pose_graphs(pose_graph1, pose_graph2, timestamp_2):
    """associate pose_graph1 to pose_graph2 according to frame_id, which are the first colomn

    Args:
        pose_graph1 (pandas dataframe): 
            frame_id    x    y    z    qx    qy    qz    qw
        pose_graph2 (pandas dataframe): 
            frame_id    x    y    z    qx    qy    qz    qw

    Returns:
        associated_pose_graph1 (pandas dataframe): a sub graph of pose_graph1
    """

    associated_pose_graph1 = pd.DataFrame(index=pose_graph2.index, columns=['frame_id', 'x', 'y', 'z', 'qx', 'qy', 'qz', 'qw'])
    ground_truthID = 0

    # if not option:
    #     for i in range(0, pose_graph2.shape[0]):
    #         pose_graph2['timestamp'][i] = 2e9-pose_graph2['timestamp'][i]

    #     pose_graph2 = pose_graph2.sort_values(by=['timestamp'])


    print(pose_graph1['timestamp'][0])
    print(type(pose_graph1['timestamp'][0]))

    for i in range(0, pose_graph2.shape[0]):
        image_id = pose_graph2['frame_id'][i]
        tracked_time = timestamp_2.iloc[image_id,0]
            

        for j in range(0, pose_graph1.shape[0]):
            if (pose_graph1['timestamp'][j] - tracked_time) > 0.001:

                associated_pose_graph1['frame_id'][ground_truthID] = image_id
                associated_pose_graph1.iloc[ground_truthID, 1:8] = pose_graph1.iloc[j, 1:8]
                ground_truthID += 1
                break


    return associated_pose_graph1



if __name__ == "__main__":
    pose_graph_1 =sys.argv[1] # groundtruth
    pose_graph_2 =sys.argv[2] # results
    timestamp_2 = sys.argv[3]
    trial_method = sys.argv[4]


    pg1 = read_pose_graph_with_timestamp(pose_graph_1)
    pg2 = read_pose_graph(pose_graph_2)
    time2 = read_timestamp_id(timestamp_2)

    
    associated_pg1 = associate_pose_graphs(pg1, pg2, time2)
    # print(associated_pg1)
    # with pd.option_context('display.precision', 15):
    #     print(pg1)
    #     print(pg2)
    #     print(associated_pg1)

    nan_rowindex = associated_pg1.loc[associated_pg1['x'].isna()].index
    associated_pg1 = associated_pg1.drop(nan_rowindex)
    pg2 = pg2.drop(nan_rowindex)


    
    end_index = associated_pg1.shape[0]
    if len(sys.argv) >5:
        end_index = int(sys.argv[5])

    print(associated_pg1.tail(1))

    print('last timestamp: ', time2.iloc[associated_pg1['frame_id'].tail(1), 0])

    gt_nparray = associated_pg1[['x', 'y', 'z']].to_numpy(dtype=float)[0:end_index, :]
    pg2_nparray = pg2[['x', 'y', 'z']].to_numpy(dtype=float)[0:end_index, :]
    # print(pg2_nparray)
    print('associated poses: ', pg2_nparray.shape)

    scale, translation, rotation, rmse = align_sim3(gt_nparray, pg2_nparray)

    print('scale: ' , scale)
    print('translation: ', translation)
    print('rotation: ', rotation)
    print('rmse: ', rmse)


    # plot_results()
    