#!/usr/bin/env python

import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

"""example:
python plane_age.py ../logs/ 0 4
"""

def read_log_file(log_file_path, host_id, plane_id, naming_template):
    """read a log file and extract the information

    Args:
        log_file_path (str): relative path

    Returns:
        
    """

    optimize_info = pd.read_csv(log_file_path, delim_whitespace=True, header = None, 
    names = ['host', 'host_id', 'plane', 'plane_id', 'a', 'age', 're', 'nRes', 'np', 'nPoints'], dtype=str)

    sub_info = optimize_info[['host_id', 'plane_id', 'age', 'nRes', 'nPoints']]
    print(sub_info. columns)
    print(sub_info.dtypes)
    sub_info = sub_info.loc[(sub_info['host_id'] == host_id) & (sub_info['plane_id'] == plane_id)] 
    
    sub_info_int = sub_info.astype(int)
    sub_info_int = sub_info_int.sort_values(by=['age'])
    sub_info_int = sub_info_int.drop_duplicates()
 
    print(sub_info_int)


    fig, ax = plt.subplots()
    plt.plot(sub_info_int['nPoints'], 'b')
    filename = 'host'+host_id+'plane'+plane_id+'_nPoints_evolution'
    print('saving plots to ', naming_template + '_' + filename)
    plt.xlabel('age')
    plt.ylabel('nPoints')
    plt.savefig(naming_template + '_' + filename)
    plt.show()

    # fig, ax = plt.subplots()
    # plt.plot(sub_info['nPlanes'], 'b')
    # filename = 'nPlanes_evolution'
    # print('saving plots to ', naming_template + '_' + filename)
    # plt.xlabel('at KFrame')
    # plt.ylabel('nPlanes')
    # plt.savefig(naming_template + '_' + filename)
    # plt.show()

    # fig, ax = plt.subplots()
    # plt.plot(sub_info['nRes'], 'b')
    # filename = 'nRes_evolution'
    # print('saving plots to ', naming_template + '_' + filename)
    # plt.xlabel('at KFrame')
    # plt.ylabel('nRes')
    # plt.savefig(naming_template + '_' + filename)
    # plt.show()


if __name__ == "__main__":

    log_folder = sys.argv[1]
    host_id = sys.argv[2]
    plane_id = sys.argv[3]
    naming_template = sys.argv[4]

    file_name = 'plane_nRes'
    if log_folder[-1]!='/':
        log_folder +='/'
    extract_age_command = 'grep \"nRes: \" systemPlaneUpdatesLog.txt > ' + file_name

    os.chdir(log_folder)
    os.system(extract_age_command)
    os.chdir('/media/amber/www/devel/dsop_ws/devel/lib/dso_plane_ros/scripts')

    read_log_file(log_folder + file_name, host_id, plane_id, naming_template)