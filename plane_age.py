#!/usr/bin/env python

import pandas as pd
import sys
import os

"""example:
python plane_age.py /media/amber/www/devel/dsop_results/nplanes1_results_newdsop_sfm_planar_2_trial0/logs/ 0 4
"""

def read_log_file(log_file_path):
    """read a log file and extract the information

    Args:
        log_file_path (str): relative path

    Returns:
        
    """

    logs = pd.read_csv(log_file_path, delim_whitespace=True, header = None, \
        names = ['host_token', 'host_id', 'plane_token', 'plane_id', 'age_token', 'age'])

    logs = logs[['host_id', 'plane_id', 'age']]
    # logs = logs.sort_values(by=['host_id', 'plane_id'])

    temp = logs.groupby(['host_id','plane_id']).max()
    print(temp)
    print('Average plane ages in this run: '+ str(temp.median()))
    print(temp.loc[0])
    temp2 = pd.concat([temp, temp.groupby(level=0).agg(['mean']).stack(1)])
    print(temp2)
    temp3 = pd.concat([temp, temp.groupby(level=0).agg(['std']).stack(1)])
    print(temp3)
    # print(logs.loc[(logs['host_id'] == int(host_id)) & (logs['plane_id'] == int(plane_id))]['age'].max())


if __name__ == "__main__":

    log_folder = sys.argv[1]
    # host_id = sys.argv[2]
    # plane_id = sys.argv[3]

    age_file_name = 'planeAge.txt'
    if log_folder[-1]!='/':
        log_folder +='/'
    extract_age_command = 'grep \"age:\" systemPlaneUpdatesLog.txt > ' + age_file_name

    os.chdir(log_folder)
    os.system(extract_age_command)
    os.chdir('/media/amber/www/devel/dsop_ws/devel/lib/dso_plane_ros/scripts')

    read_log_file(log_folder +age_file_name)


