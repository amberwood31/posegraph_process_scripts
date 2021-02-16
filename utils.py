#!/usr/bin/env python

import pandas as pd
import numpy as np

def read_pose_graph(pose_graph_path):
    """[summary]

    Args:
        pose_graph_path (str): [description]
    
    Returns:
        pose_graph (pandas dataframe): 
            frame_id    x    y    z    qx    qy    qz    qw

    """
    pose_graph = pd.read_csv(pose_graph_path, delim_whitespace=True , header = None, names = ['frame_id', 'x', 'y', 'z', 'qx', 'qy', 'qz', 'qw']) 

    return pose_graph

def read_pose_graph_with_timestamp(pose_graph_path):
    """[summary]

    Args:
        pose_graph_path (str): [description]
    
    Returns:
        pose_graph (pandas dataframe): 
            frame_id    x    y    z    qx    qy    qz    qw

    """
    pose_graph = pd.read_csv(pose_graph_path, delim_whitespace=True , header = None, names = ['timestamp', 'x', 'y', 'z', 'qx', 'qy', 'qz', 'qw']) 

    return pose_graph

def compute_odometry(position_array):
    """ compute the relative position from absolute position

    Args:
        position_array (numpy_array): [description]
    """

    rel_position = np.diff(position_array, axis=0)

    return rel_position
