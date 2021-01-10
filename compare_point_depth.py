import argparse
import sys
import numpy as np
import math

"""example_scripts

python compare_point_depth.py ../results_dsop10_500_images/host0_age0.uvdepth /media/amber/www/data/ICL_living_room_traj0_frei_png/depth_pov/scene_00_0000.depth
"""

def parse_arguments():
    return args

def read_uvdepth_file(file_name):
    """read a uvdepth file with the pattern u v idepth

    Args:
        file_name ([type]): [description]

    Returns:
        [type]: [description]
    """

    uv_idepth_array = np.loadtxt(file_name, dtype = 'str', delimiter=' ')
    return uv_idepth_array

def read_scenedepth_file(file_name):
    """read a pov depth file with only pov depth, following image row-major direction

    Args:
        file_name ([type]): [description]

    Returns:
        [type]: [description]
    """
    scenedepth_array = np.loadtxt(file_name, dtype = 'str', delimiter=' ')

    return scenedepth_array


if __name__ == "__main__":

    img_height = 480
    img_width = 640
    cx = 319.50
    cy = 239.50
    fx = 481.20
    fy = -480.00


    file1 =sys.argv[1]
    file2 = sys.argv[2]
    uv_idepth_array = read_uvdepth_file(file1)
    scene_depth_array = read_scenedepth_file(file2)
    print('estimating ', uv_idepth_array.shape[0], ' points')

    diff_depth = np.zeros(uv_idepth_array.shape[0])
    for index in range(0, uv_idepth_array.shape[0]):
        item = uv_idepth_array[index]
        u = int(item[0])
        v = int(item[1])
        idepth = float(item[2])
        #print(u, v, 'idepth: ', idepth)
        pixel_index = u + v*img_width
        #print('index: ', index)
        pov_depth = float(scene_depth_array[pixel_index])

        u_u0_by_fx = (u-cx)/fx
        v_v0_by_fy = (v-cy)/fy

        depth_gt = pov_depth / math.sqrt(u_u0_by_fx*u_u0_by_fx +       v_v0_by_fy*v_v0_by_fy + 1 ) 
        #print('depth_gt: ', depth_gt)

        depth_estimated = 1/idepth
        #print('depth_estimate: ', depth_estimated)
        diff_depth[index] = abs(depth_estimated - depth_gt)

    print(diff_depth.mean())






    




