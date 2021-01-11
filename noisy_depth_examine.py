import argparse
import sys
import numpy as np
import math
import cv2

"""example_scripts

python noisy_depth_examine.py /media/amber/www/data/ICL_living_room_traj0_frei_png/depth_pov/scene_00_0100.depth /media/amber/www/data/ICL_living_room_traj0n_frei_png/depth/00100.png 400 100
"""


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

def read_icldepth_file(file_name):

    depth_unit16 = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    depth = depth_unit16.astype('float') / 5000.0

    return depth


if __name__ == "__main__":

    img_height = 480
    img_width = 640
    cx = 319.50
    cy = 239.50
    fx = 481.20
    fy = -480.00


    file1 =sys.argv[1]
    file2 = sys.argv[2]
    u = int(sys.argv[3])
    v = int(sys.argv[4])
    
    scene_depth_array = read_scenedepth_file(file1)
    icl_depth = read_icldepth_file(file2)

    pixel_index = u + v*img_width
    pov_depth = float(scene_depth_array[pixel_index])
    u_u0_by_fx = (u-cx)/fx
    v_v0_by_fy = (v-cy)/fy

    depth_frompov = pov_depth / math.sqrt(u_u0_by_fx*u_u0_by_fx + v_v0_by_fy*v_v0_by_fy + 1 ) 

    depth_fromicl = icl_depth[v,u]
    print('pov depth of ', u, ' ', v, ': ', depth_frompov, 'converted noisy depth: ', depth_fromicl)







    




