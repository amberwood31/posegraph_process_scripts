#run pcl_point_selection scripts for different planes over time
#plot selected_pointcloud with DSOP planar pointcloud to compare the performance over time

import os
import argparse


frame_id = 0
plane_id = 4
age_id = 2

def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze and plot point depth optimization performance')
    parser.add_argument('-frame', dest='frame', help='frame ID',
                        default=0, type=int)
    parser.add_argument('-plane', dest='plane', help='plane ID',
                        default=0, type=int)
    parser.add_argument('-age', dest='age', help='results age',
                        default=0, type=int)

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    
    options = parse_arguments()

    frame_id = options.frame
    plane_id = options.plane
    age_id = options.age

    point_select_command = './pcl_point_select '
    point_select_command += 'results_dso/'
    point_select_command += 'pcd_frame' + str(frame_id)
    point_select_command += '_age' + str(age_id)
    point_select_command += '.uvdepth results_initialization_with_derived/host'+str(frame_id)
    point_select_command += '_plane' + str(plane_id)+'.csv '
    point_select_command +='results_dso/'
    point_select_command += 'pcd_frame' + str(frame_id) + '_age' +str(age_id)

    point_select_file_name = 'selected_point_frame' + str(frame_id) + '_plane'+ str(plane_id) + '_age' + str(age_id) + '.pcd'
    point_select_command += ' ' + point_select_file_name

    os.system(point_select_command)

    plot_command = 'pcl_viewer -bc 1,1,1 -ps 10 results_initialization_with_derived/pcd_frame' + str(frame_id) + '_plane' + str(plane_id) + '_age' + str(age_id) + '.pcd -ps 10 ' + point_select_file_name + ' -ax 1'

    os.system(plot_command)



