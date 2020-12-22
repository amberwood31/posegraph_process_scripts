#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits import mplot3d

# In[2]:
plot_node_degree = False
plot_all_lc = False
plot_3d_to_2d = True

def plot_trajectory( file_name , options, end_vertex=1508):
#options = "2d"
#file_name = "/home/amber/stew/test_backend/manhattan_group10_outlier1000_vertigo/manhattan_seed_7/input.g2o"
#print(file_name)
    df = pd.read_csv(file_name, sep = "\s+|\t+|\s+\t+|\t+\s+" , header = None, names = range(12)) #
    
    if options == "2d":
        vertex = df.loc[df[0] == "VERTEX_SE2"]
        edges = df.loc[df[0] == "EDGE_SE2"]
    elif options == "3d":
        vertex = df.loc[df[0] == "VERTEX_SE3:QUAT"]
        edges = df.loc[df[0] == "EDGE_SE3:QUAT"]
    elif options == "ICL":
        vertex = df

    # In[]:
        # Don't do sorting here. Intermediate pose graph outputs from rtabmap had the reversed vertex_id
        # but the actual poses are in increasing sequencial. Just ignore the vertex_id
    #vertex = vertex.sort_values(by = 1) # sorting vertex indexes to be increasing sequencial
    #vertex = vertex.reset_index(drop=True) # refresh the index
    print(vertex)
    trajectory_x = np.array(vertex[1]) # 2D_trajectory_x
    print(trajectory_x)
    trajectory_y = np.array(vertex[2]) # 2D_trajectory_y
    if options == "3d":
        trajectory_z = np.array(vertex[3])
    
    fig, ax = plt.subplots()
    if options == "2d":
        plt.plot(trajectory_x[0:end_vertex], trajectory_y[0:end_vertex], 'b')
    elif options in ["3d", "ICL"]:
        if plot_3d_to_2d == True:
            plt.plot(trajectory_x[0:end_vertex], trajectory_y[0:end_vertex], 'b')
            plt.plot(trajectory_x[0:100], trajectory_y[0:100], 'r')


        else:
            ax = plt.axes(projection='3d')
            ax.plot3D(trajectory_x[0:end_vertex], trajectory_y[0:end_vertex], trajectory_z[0:end_vertex], 'gray')
        
    plt.axis('equal')
    #default_size = fig.get_size_inches()
    #fig.set_size_inches( (default_size[0]*0.5, default_size[1]*0.8) )
    #print('default_size: ', default_size)
    #ax.axis('off') #diable border
    #plt.axis((-300,300,-10,500))
    filename = file_name.split(".")
    plt.savefig(filename[0])
    plt.show()

# In[3]:

print ('READ g2o file: ' + str(sys.argv[1]))
if len(sys.argv) < 3:
    plot_trajectory(str(sys.argv[1]), 'ICL')
elif len(sys.argv) == 3:
    plot_trajectory(str(sys.argv[1]), 'ICL', int(sys.argv[2]))




# In[ ]:





# In[ ]:




                                                       


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




