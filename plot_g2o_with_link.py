#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits import mplot3d
from utils import read_pose_graph
from utils import compute_odometry

# In[2]:
plot_node_degree = False
plot_all_lc = False
plot_3d_to_2d = False
plot_option = '3d'

def plot_trajectory( file_name , options, dataset):
#options = "2d"
#file_name = "/home/amber/stew/test_backend/manhattan_group10_outlier1000_vertigo/manhattan_seed_7/input.g2o"
#print(file_name)
    df = read_pose_graph(file_name)
    
    if dataset == 'ICL':
        vertex = df
    elif options == "2d":
        vertex = df.loc[df[0] == "VERTEX_SE2"]
        edges = df.loc[df[0] == "EDGE_SE2"]
    elif options == "3d":
        vertex = df.loc[df[0] == "VERTEX_SE3:QUAT"]
        edges = df.loc[df[0] == "EDGE_SE3:QUAT"]

    # In[]:
        # Don't do sorting here. Intermediate pose graph outputs from rtabmap had the reversed vertex_id
        # but the actual poses are in increasing sequencial. Just ignore the vertex_id
    #vertex = vertex.sort_values(by = 1) # sorting vertex indexes to be increasing sequencial
    #vertex = vertex.reset_index(drop=True) # refresh the index
    end_vertex = vertex.shape[0]
    vertex_selected = vertex.iloc[0:end_vertex]
    trajectory_selected = vertex_selected[['x','y','z']].to_numpy()
    trajectory_x = trajectory_selected[:,0] # 2D_trajectory_x
    print('trajectory x: ', trajectory_x)
    trajectory_y = trajectory_selected[:,1] # 2D_trajectory_y
    if options == "3d":
        trajectory_z = trajectory_selected[:,2]
        print('trajectory z: ', trajectory_z)
    
    fig, ax = plt.subplots()
    if options == "2d":
        plt.plot(trajectory_x[0:end_vertex], trajectory_y[0:end_vertex], 'b')
    elif options == '3d':
        if plot_3d_to_2d == True:
            plt.plot(trajectory_x[0:end_vertex], trajectory_y[0:end_vertex], 'b')
            plt.plot(trajectory_x[0:100], trajectory_y[0:100], 'r')


        else:
            ax = plt.axes(projection='3d')
            ax.plot3D(trajectory_x, trajectory_y, trajectory_z, 'gray')
            ax.plot3D(trajectory_x[0:20], trajectory_y[0:20], trajectory_z[0:20], 'red')
        
    plt.axis('equal')
    #default_size = fig.get_size_inches()
    #fig.set_size_inches( (default_size[0]*0.5, default_size[1]*0.8) )
    #print('default_size: ', default_size)
    #ax.axis('off') #diable border
    #plt.axis((-300,300,-10,500))
    filename = file_name.split(".")
    print('saving plots to ', filename[0])
    plt.savefig(filename[0])
    plt.show()

    camera_movement = compute_odometry(trajectory_selected)
    fig, ax = plt.subplots()
    plt.plot(camera_movement[:,0], 'r')
    plt.plot(camera_movement[:,1], 'g')
    plt.plot(camera_movement[:,2], 'b')
    filename = 'camera_movement'
    plt.savefig(filename)
    plt.show()


# In[3]:

print ('READ g2o file: ' + str(sys.argv[1]))
if len(sys.argv) < 3:
    plot_trajectory(str(sys.argv[1]), plot_option, 'ICL')
elif len(sys.argv) == 3:
    plot_trajectory(str(sys.argv[1]), plot_option, 'ICL', int(sys.argv[2]))




# In[ ]:





# In[ ]:




                                                       


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




