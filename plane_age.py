#!/usr/bin/env python

import pandas as pd
import sys

def read_log_file(log_file_path, host_id, plane_id):
    """read a log file and extract the information

    Args:
        log_file_path (str): relative path

    Returns:
        
    """

    logs = pd.read_csv(log_file_path, delim_whitespace=True, header = None, \
        names = ['host_token', 'host_id', 'plane_token', 'plane_id', 'age_token', 'age'])

    logs = logs.sort_values(by=['host_id', 'plane_id'])

    print(logs.loc[(logs['host_id'] == int(host_id)) & (logs['plane_id'] == int(plane_id))])


if __name__ == "__main__":

    log_file = sys.argv[1]
    host_id = sys.argv[2]
    plane_id = sys.argv[3]
    read_log_file(log_file, host_id, plane_id)