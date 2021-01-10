#run pcl_point_selection scripts for different planes over time
#plot selected_pointcloud with DSOP planar pointcloud to compare the performance over time

import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze and plot point depth optimization performance')
    parser.add_argument('-frame', dest='frame', help='frame ID',
                        default=0, type=int)
    parser.add_argument('-plane', dest='plane', help='a list plane ID',
                        default="4", type=str)
    parser.add_argument('-age', dest='age', help='results age',
                        default=0, type=int)

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    
    options = parse_arguments()

    frame_id = options.frame
    plane_id_list = [int(item) for item in options.plane.split(',')]

    dso_results_dir = '../results_dso_500_images/'
    new_results_dir = '../results_dsop10_500_images/'

    point_select_file_name_list = []
    for plane_id in plane_id_list:
        age_id = options.age


        # this command select the planar points from the DSO results and save to a file
        point_select_command = './pcl_point_select '
        point_select_command += dso_results_dir
        point_select_command += 'host' + str(frame_id)
        point_select_command += '_age' + str(age_id)
        point_select_command += '.uvdepth '
        point_select_command += new_results_dir
        point_select_command += 'host'+str(frame_id)
        point_select_command += '_plane' + str(plane_id)+'_newestKF' + str(age_id) + '_coordinates.csv '
        point_select_command += dso_results_dir
        point_select_command += 'host' + str(frame_id) + '_age' 
        point_select_command += str(age_id) + '.camera'

        point_select_file_name = 'selected_point_frame' + str(frame_id) + '_plane'+ str(plane_id) + '_age' + str(age_id) + '.pcd'
        point_select_file_name_list.append(point_select_file_name)
        point_select_command += ' ' + point_select_file_name

        os.system(point_select_command)
        print('ran command', point_select_command)


    plot_command = 'pcl_viewer -bc 1,1,1 -ps 10'

    for plane_id in plane_id_list:
        point_select_file_name = 'selected_point_frame' + str(frame_id) + '_plane'+ str(plane_id) + '_age' + str(age_id) + '.pcd'
        plot_command += ' ' + new_results_dir + 'pcd_frame' + str(frame_id) + '_plane' + str(plane_id) + '_age' + str(age_id) + '.pcd -ps 10 -ax 1 '
        plot_command += point_select_file_name + ' -ps 10 -ax 1'

    print(plot_command)
    os.system(plot_command)



