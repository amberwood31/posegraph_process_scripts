import cv2
import argparse
import pandas as pd
import os

"""example
python plot_image_with_specific_pixel_marked.py -image /media/amber/www/data/ICL_living_room_traj0_frei_png/rgb/00000.png -pixel_file ../newlog_dsop_living0/host0_plane4_coordinates.csv ../newlog_dsop_living0/host0_plane6_coordinates.csv ../newlog_dsop_living0/host0_plane7_coordinates.csv ../newlog_dsop_living0/host0_plane9_coordinates.csv -file_type original -nonplanar_file ../newlog_dsop_living0/host0_age0_nonplanar.uv 

python plot_image_with_specific_pixel_marked.py -image /media/amber/www/data/ICL_living_room_traj0_frei_png/rgb/00141.png -pixel_file ../newlog_dsop_living0/afterRemoval_host0_target9_plane4_projected.csv ../newlog_dsop_living0/afterRemoval_host0_target9_plane6_projected.csv ../newlog_dsop_living0/afterRemoval_host0_target9_plane7_projected.csv -file_type projected

python plot_image_with_specific_pixel_marked.py -image /media/amber/www/data/ICL_living_room_traj0_frei_png/rgb/00224.png -pixel_file ../newlog_dsop_living0/afterRemoval_host0_target18_plane7_projected.csv -file_type projected

python plot_image_with_specific_pixel_marked.py -image /media/amber/www/data/ICL_living_room_traj0_frei_png/rgb/00265.png -pixel_file ../newlog_dsop_living0/host23_plane3_newestKF24_coordinates.csv ../newlog_dsop_living0/host23_plane9_newestKF24_coordinates.csv -file_type original -nonplanar_file ../newlog_dsop_living0/host23_age24_nonplanar.uv 


"""

color = [(0, 0, 255), (0,255,255), (255, 0, 255), (255,0,0)]

def parse_arguments():
    parser = argparse.ArgumentParser(description='PlotImage')
    parser.add_argument('-image', dest='image', help='image to plot',
                        default='image00', type=str)
    # parser.add_argument('-u', dest='u', help='image pixel to mark',
    #                     default=0, type=int)
    # parser.add_argument('-v', dest='v', help='image pixel to mark',
    #                     default=0, type=int)

    parser.add_argument('-pixel_file', dest='pixel_file', nargs='+', help='file that stores pixel coordinates', required=True)
    # parser.add_argument('-pixel_file', dest='pixel_file', help='file that stores pixel coordinates', default='pixel_file', type=str)
    parser.add_argument('-nonplanar_file', dest='nonplanar_file', help='pixel file of nonplanar points', 
                        default='nonplanar_file', type=str)
    parser.add_argument('-file_type', dest='file_type', help='could be original pixel file or \
    projected', default='original', type=str)

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    options = parse_arguments()

    img = cv2.imread(options.image)

    # cv2.drawMarker(img, (options.u, options.v), (0, 0, 255), markerType=cv2.MARKER_STAR,
    #                markerSize=40, thickness=2, line_type=cv2.LINE_AA)
    
    if options.file_type == 'projected':     
        color_index = 0    
        for single_file in options.pixel_file:
            pixel_filepath_list = single_file.split('/')
            pixel_file_name = pixel_filepath_list[-1]
            pixel_file_folder = single_file.replace(pixel_filepath_list[-1],'')
            extract_coordinates_command = 'grep \"host\" ' + pixel_file_name + '> ' + pixel_file_name[-34::]

            print('entering folder', pixel_file_folder)
            current_dir = os.getcwd()
            os.chdir(pixel_file_folder)
            print('run command', extract_coordinates_command)
            os.system(extract_coordinates_command)
            os.chdir(current_dir)
            print('read file', pixel_file_folder+pixel_file_name[-34::])
            df = pd.read_csv(pixel_file_folder+pixel_file_name[-34::], sep=' ', header=None)
            pixels = df.to_numpy()

            print('marking '+ str(pixels.shape[0]) + ' pixels')

            for item in pixels:

                if (round(item[6]) > 640) or (round(item[7]) > 480) or item[6] < 0 or item[7] < 0:
                    continue

                cv2.drawMarker(img, (int(round(item[6])), int(round(item[7]))), color[color_index], markerType=cv2.MARKER_DIAMOND,
                        markerSize=20, thickness=2, line_type=cv2.LINE_AA)
            color_index +=1

    elif options.file_type == 'original':
        color_index = 0
        for single_file in options.pixel_file:
            df = pd.read_csv(single_file, sep=' ', header=None)

            pixels = df.to_numpy()

            print('marking '+ str(pixels.shape[0]) + ' pixels')

            for item in pixels:
                cv2.drawMarker(img, (item[0], item[1]), color[color_index], markerType=cv2.MARKER_DIAMOND,
                            markerSize=20, thickness=2, line_type=cv2.LINE_AA)

            color_index +=1
        
        df2 = pd.read_csv(options.nonplanar_file, sep=' ', header=None)
        nonplanar_pixels = df2.to_numpy()
        print('marking '+ str(nonplanar_pixels.shape[0]) + ' nonplanar pixels')

        for item in nonplanar_pixels:
            cv2.drawMarker(img, (int(item[0]), int(item[1])), (0, 255, 0), markerType=cv2.MARKER_CROSS,
                            markerSize=20, thickness=2, line_type=cv2.LINE_AA)
                

    save_file = 'marked_image.png'
    print('saving to '+ save_file)

    cv2.imshow('marked_pixel', img)
    cv2.waitKey(0)
    cv2.imwrite(save_file, img)

