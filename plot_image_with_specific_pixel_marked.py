import cv2
import argparse
import pandas as pd

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

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    options = parse_arguments()

    img = cv2.imread(options.image)

    cv2.drawMarker(img, (options.u, options.v), (0, 0, 255), markerType=cv2.MARKER_STAR,
                   markerSize=40, thickness=2, line_type=cv2.LINE_AA)

    df = pd.read_csv(options.pixel_file, sep=' ', header=0)
    pixels = df.to_numpy()

    print('marking '+ str(pixels.size) + ' pixels')

    for item in pixels:
        cv2.drawMarker(img, (item[0], item[1]), (0, 0, 255), markerType=cv2.MARKER_STAR,
                       markerSize=20, thickness=2, line_type=cv2.LINE_AA)

    save_file = options.pixel_file[-28:-4]+'.png'
    print('saving to '+ save_file)
    cv2.imwrite(save_file, img)


