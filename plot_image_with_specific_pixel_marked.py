import cv2
import argparse
import pandas as pd
import os

"""example
python plot_image_with_specific_pixel_marked.py -image ../../predict/4_segmentation_pred_blended_0.png -pixel_file ../host4_plane6_coordinates.csv -file_type original

or
python plot_image_with_specific_pixel_marked.py -image ../../predict/2_segmentation_pred_blended_0.png -pixel_file ../afterRemoval_host0_target2_plane9_projected.csv -file_type projected

"""

def parse_arguments():
    parser = argparse.ArgumentParser(description='PlotImage')
    parser.add_argument('-image', dest='image', help='image to plot',
                        default='image00', type=str)
    parser.add_argument('-u', dest='u', help='image pixel to mark',
                        default=0, type=int)
    parser.add_argument('-v', dest='v', help='image pixel to mark',
                        default=0, type=int)

    parser.add_argument('-pixel_file', dest='pixel_file', help='file that stores pixel coordinates',
                        default='pixel_file', type=str)

    parser.add_argument('-file_type', dest='file_type', help='could be original pixel file or \
    projected', default='original', type=str)

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    options = parse_arguments()

    img = cv2.imread(options.image)

    cv2.drawMarker(img, (options.u, options.v), (0, 0, 255), markerType=cv2.MARKER_STAR,
                   markerSize=40, thickness=2, line_type=cv2.LINE_AA)
    
    if options.file_type == 'projected':         
        pixel_filepath_list = options.pixel_file.split('/')
        pixel_file_name = pixel_filepath_list[-1]
        pixel_file_folder = options.pixel_file.replace(pixel_filepath_list[-1],'')
        extract_coordinates_command = 'grep \"host\" ' + pixel_file_name + '> ' + pixel_file_name[-34::]

        print('entering folder', pixel_file_folder)
        os.chdir(pixel_file_folder)
        print('run command', extract_coordinates_command)
        os.system(extract_coordinates_command)
        os.chdir('/media/amber/www/devel/dsop_ws/devel/lib/dso_plane_ros/scripts')
        print('read file', pixel_file_folder+pixel_file_name[-34::])
        df = pd.read_csv(pixel_file_folder+pixel_file_name[-34::], sep=' ', header=None)
        pixels = df.to_numpy()
    elif options.file_type == 'original':
        df = pd.read_csv(options.pixel_file, sep=' ', header=None)
        pixels = df.to_numpy()

    print('marking '+ str(pixels.shape[0]) + ' pixels')

    for item in pixels:
        if options.file_type == 'original':
            cv2.drawMarker(img, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                       markerSize=20, thickness=2, line_type=cv2.LINE_AA)
        elif options.file_type == 'projected':
            
            if (round(item[6]) > 640) or (round(item[7]) > 480) or item[6] < 0 or item[7] < 0:
                continue

            cv2.drawMarker(img, (int(round(item[6])), int(round(item[7]))), (0, 0, 255), markerType=cv2.MARKER_STAR,
                    markerSize=20, thickness=2, line_type=cv2.LINE_AA)



    if options.file_type == 'original':
        save_file = options.pixel_file[-28:-4]+'.png'
    elif options.file_type == 'projected':
        save_file = options.pixel_file[-34:-4]+'.png'
    print('saving to '+ save_file)
    cv2.imwrite(save_file, img)

