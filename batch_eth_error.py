#!/usr/bin/env python

import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from utils import read_pose_graph, read_timestamp_id, read_pose_graph_with_timestamp
from error import align_sim3, plot_aligned_array_together 
from batch_eth_experiment import input_filenames, trials, gt_path
from eth_error import associate_pose_graphs


"""example
 python eth_error.py /media/amber/www/data/sfm_planar_2/groundtruth.txt /media/amber/www/devel/dsop_results/trial_nplane1_dsop_sfm_planar2/result.txt /media/amber/www/data/sfm_planar_2/rgb.txt test

"""

"""some configuration variables"""
results_dir = '/media/amber/www/devel/dsop_results/'
output_folder_name_templete = 'nplanes1_results_newdsop_'
output_folder_name_templete = 'dso_results_newdsop_'




if __name__ == "__main__":
    name_template = ''
    if len(sys.argv) > 1:
        name_template = sys.argv[1]


    output_path = []
    columns_name = []
    for i in range(0, len(input_filenames)):

        input_template = input_filenames[i]
        column_input = input_template

        path = output_folder_name_templete + input_template

        if i%2 == 1:
            path = path + '_reverse'
            column_input += '_reverse'

        columns_name.append(column_input)
        output_path.append(path)

    scale_dataframe = pd.DataFrame(index = range(0,trials), columns = columns_name)
    translation_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    rotation_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    rmse_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    
    for j in range(0, len(input_filenames)):
        for i in range(0,trials):

            results_folder_name = output_path[j] + '_trial' + str(i)
            gt_graph = gt_path[j] + '/groundtruth.txt'
            results_graph = results_dir + results_folder_name + '/result.txt'
            time_file = gt_path[j] + '/rgb.txt'

            try:
                print('processing: ', results_folder_name)
                pg1 = read_pose_graph_with_timestamp(gt_graph)
                pg2 = read_pose_graph(results_graph)
                time2 = read_timestamp_id(time_file)

                
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
                if len(sys.argv) >2:
                    end_index = int(sys.argv[2])

                gt_nparray = associated_pg1[['x', 'y', 'z']].to_numpy(dtype=float)[0:end_index, :]
                pg2_nparray = pg2[['x', 'y', 'z']].to_numpy(dtype=float)[0:end_index, :]
                # print(pg2_nparray)
                print('associated poses: ', pg2_nparray.shape)

                scale, translation, rotation, rmse = align_sim3(gt_nparray, pg2_nparray)

                print('scale: ' , scale)
                print('translation: ', translation)
                print('rotation: ', rotation)
                print('rmse: ', rmse)

                scale_dataframe.iloc[i, j] = scale
                translation_dataframe.iloc[i, j] = translation
                rotation_dataframe.iloc[i,j] = rotation
                rmse_dataframe.iloc[i,j] = rmse
            except:
                    
                scale_dataframe.iloc[i, j] = float('nan')
                translation_dataframe.iloc[i, j] = float('nan')
                rotation_dataframe.iloc[i,j] = float('nan')
                rmse_dataframe.iloc[i,j] = float('nan')
                continue

    print('writing to: ', name_template + '_eth_scale.csv')
    scale_dataframe.to_csv(name_template + '_eth_scale.csv')
    translation_dataframe.to_csv(name_template + '_eth_translation.csv')
    rotation_dataframe.to_csv(name_template + '_eth_rotation.csv')
    rmse_dataframe.to_csv(name_template + '_eth_rmse.csv')
    