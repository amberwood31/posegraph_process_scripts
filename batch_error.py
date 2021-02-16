#!/usr/bin/env python

import pandas as pd
import numpy as np
from utils import read_pose_graph

from error import associate_pose_graphs, plot_aligned_array_together, align_sim3
from batch_experiment import input_filenames, gt_path, trials, results_folder_template, output_folder_name_templete
import sys

print(input_filenames)
print('trials', trials)


if __name__ == "__main__":
    name_template = ''
    if len(sys.argv) >1:
        name_template = sys.argv[1]

    
    output_path = []
    columns_name = []
    for i in range(0, len(input_filenames)):

        input_template = input_filenames[i]
        column_input = input_template

        path = output_folder_name_templete + 'results_newdsop_' + input_template

        if i%2 == 1:
            path = path + '_reverse'
            column_input += '_reverse'

        columns_name.append(column_input)
        output_path.append(path)


    # print(output_path)

    scale_dataframe = pd.DataFrame(index = range(0,trials), columns = columns_name)
    translation_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    rotation_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    rmse_dataframe = pd.DataFrame(index = range(0, trials), columns = columns_name)
    
    for j in range(0, len(input_filenames)): #

        for i in range(0, trials):
            
            # get experimental results folder
            results_folder_name = output_path[j] + '_trial' + str(i)
            gt_graph = '../' + gt_path[j] + '/groundtruth.txt'
            results_graph = '../' + results_folder_name + '/result.txt'

            try:
                print('procesing ', results_folder_name)
                gt_pose = read_pose_graph(gt_graph)
                results_pose = read_pose_graph(results_graph)

                associated_gtpose = associate_pose_graphs(gt_pose, results_pose)

                results_pose = results_pose.loc[results_pose['frame_id'].isin(associated_gtpose['frame_id']).tolist()]

                if j%2 == 1: # these runs are backward
                    results_pose = results_pose[::-1].reset_index()
                end_index = associated_gtpose.shape[0]
                if len(sys.argv) >2:
                    end_index = int(sys.argv[2])
                gt_nparray = associated_gtpose[['x', 'y', 'z']].to_numpy()[0:end_index, :]
                results_nparray = results_pose[['x', 'y', 'z']].to_numpy()[0:end_index, :]
                scale, translation, rotation, rmse = align_sim3(gt_nparray, results_nparray)
                                    
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


    
    print('writing to: ', name_template + '_scale.csv')
    scale_dataframe.to_csv(name_template + '_scale.csv')
    translation_dataframe.to_csv(name_template + '_translation.csv')
    rotation_dataframe.to_csv(name_template + '_rotation.csv')
    rmse_dataframe.to_csv(name_template + '_rmse.csv')