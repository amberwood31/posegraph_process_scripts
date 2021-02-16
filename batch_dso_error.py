#!/usr/bin/env python

import pandas as pd
import numpy as np
from utils import read_pose_graph_with_timestamp

from dso_error import associate_pose_graphs, plot_aligned_array_together, align_sim3
from batch_experiment import dso_filenames, trials
import sys

gt_path_dir = '/media/amber/www/data/dso_supp_v2/gtFiles/'
results_path_dir = '/media/amber/www/data/dso_supp_v2/'

if __name__ == "__main__":

    name_template = ''
    if len(sys.argv) >1:
        name_template = sys.argv[1]
    
    results_path = []
    columns_name = []
    for i in range(0, len(dso_filenames)):

        column_input = dso_filenames[i]

        if i%2 == 0:
            path = results_path_dir + 'DS-VO_Forward/' + dso_filenames[i] 
        else:
            path = results_path_dir + 'DS-VO_Backward/' + dso_filenames[i]
            column_input += '_reverse'

        columns_name.append(column_input)
        results_path.append(path)

    # print(output_path)

    scale_dataframe = pd.DataFrame(index = range(0,trials), columns = columns_name)
    translation_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    rotation_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    rmse_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    
    for j in range(0, len(dso_filenames)): #

        for i in range(0, trials):
            
            # get experimental results folder
            gt_graph = gt_path_dir + dso_filenames[j] + '.txt'
            results_graph = results_path[j] + '_' + str(i) + '.txt'

            gt_pose = read_pose_graph_with_timestamp(gt_graph)
            results_pose = read_pose_graph_with_timestamp(results_graph)

            associated_gtpose = associate_pose_graphs(gt_pose, results_pose)

            nan_rowindex = associated_gtpose.loc[associated_gtpose['x'].isna()].index
            associated_gtpose = associated_gtpose.drop(nan_rowindex)
            results_pose = results_pose.drop(nan_rowindex)

            end_index = associated_gtpose.shape[0]
            if len(sys.argv) >2:
                end_index = int(sys.argv[2])
            gt_nparray = associated_gtpose[['x', 'y', 'z']].to_numpy(dtype=float)[0:end_index, :]
            results_nparray = results_pose[['x', 'y', 'z']].to_numpy(dtype=float)[0:end_index, :]
            try:
                scale, translation, rotation, rmse = align_sim3(gt_nparray, results_nparray)
            except:
                scale_dataframe.iloc[i, j] = float('nan')
                translation_dataframe.iloc[i, j] = float('nan')
                rotation_dataframe.iloc[i,j] = float('nan')
                rmse_dataframe.iloc[i,j] = float('nan')
                continue
                                
            print('processing ', dso_filenames[j], ' trial ', i)

            scale_dataframe.iloc[i, j] = scale
            translation_dataframe.iloc[i, j] = translation
            rotation_dataframe.iloc[i,j] = rotation
            rmse_dataframe.iloc[i,j] = rmse


    scale_dataframe.to_csv(name_template + '_dso_scale.csv')
    translation_dataframe.to_csv(name_template + '_dso_translation.csv')
    rotation_dataframe.to_csv(name_template + '_dso_rotation.csv')
    rmse_dataframe.to_csv(name_template + '_dso_rmse.csv')