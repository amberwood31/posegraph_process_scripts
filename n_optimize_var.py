#!/usr/bin/env python

import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

"""example:
python n_optimize_var.py ../logs 150 test
"""

def read_log_file(log_file_path, naming_template):
    """read a log file and extract the information

    Args:
        log_file_path (str): relative path

    Returns:
        
    """

    optimize_info = pd.read_csv(log_file_path, delim_whitespace=True, header = None, 
    names = ['OPT', 'nPoints', 'pts', 'nPlanes', 'pls', 'nRes', 'ac', 're', 'nLRes', 'li', 'res', 'newest', 'KID', 'RID', 'SID'])

    sub_info = optimize_info[['nPoints', 'nPlanes', 'nRes', 'KID', 'RID']]
    # if (host_id == 0):
    #     print('no optimization done on host 0')
    # else:
    #     nPoints_series = sub_info.loc[sub_info['KID'] == 'K' + str(host_id)+',', 'nPoints']
    #     nPlanes_series = sub_info.loc[sub_info['KID'] == 'K' + str(host_id)+',', 'nPlanes']
    #     nRes_series = sub_info.loc[sub_info['KID'] == 'K' + str(host_id)+',', 'nRes']
    #     RID_series = sub_info.loc[sub_info['KID'] == 'K' + str(host_id)+',', 'RID']
 

    #     nPoints_str = nPoints_series.values[0]
    #     nPlanes_str = nPlanes_series.values[0]
    #     nRes_str = nRes_series.values[0]
    #     frameID_str = RID_series.values[0]

    
    # print('after adding host ', host_id, ' frame ',  frameID_str, ' nPoints: ', nPoints_str, 'nPlanes: ', nPlanes_str, 'nRes: ', nRes_str)

    fig, ax = plt.subplots()
    plt.plot(sub_info['nPoints'], 'b')
    filename = 'nPoints_evolution'
    print('saving plots to ', naming_template + '_' + filename)
    plt.xlabel('at KFrame')
    plt.ylabel('nPoints')
    plt.savefig(naming_template + '_' + filename)
    plt.show()

    fig, ax = plt.subplots()
    plt.plot(sub_info['nPlanes'], 'b')
    filename = 'nPlanes_evolution'
    print('saving plots to ', naming_template + '_' + filename)
    plt.xlabel('at KFrame')
    plt.ylabel('nPlanes')
    plt.savefig(naming_template + '_' + filename)
    plt.show()

    fig, ax = plt.subplots()
    plt.plot(sub_info['nRes'], 'b')
    filename = 'nRes_evolution'
    print('saving plots to ', naming_template + '_' + filename)
    plt.xlabel('at KFrame')
    plt.ylabel('nRes')
    plt.savefig(naming_template + '_' + filename)
    plt.show()


if __name__ == "__main__":

    log_folder = sys.argv[1]
    # host_id = sys.argv[2]
    naming_template = sys.argv[1]

    file_name = 'nPoints_nPlanes'
    if log_folder[-1]!='/':
        log_folder +='/'
    extract_age_command = 'grep \"OPTIMIZE \" numsLog.txt > ' + file_name

    os.chdir(log_folder)
    os.system(extract_age_command)
    os.chdir('/media/amber/www/devel/dsop_ws/devel/lib/dso_plane_ros/scripts')

    read_log_file(log_folder + file_name, naming_template)