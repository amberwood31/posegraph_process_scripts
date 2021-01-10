
import argparse
import os
import pandas as pd

# example scripts
# python compare_point_depth.py -results ../results_dsop10_500_images/ -host 0 -age 0 -color g
# python compare_point_depth.py -results ../results_dso_500_images/ -host 0 -age 0 -color b

def parse_arguments():
    parser = argparse.ArgumentParser(description='Compare the point depth results from different sources')
    parser.add_argument('-results', dest='results', help='results folder path',
                        default='', type=str)
    parser.add_argument('-host', dest='host', help='host KF ID',
                        default=0, type=int)
    parser.add_argument('-age', dest='age', help='results age, should be at least 1+host_id',
                        default=0, type=int)
    parser.add_argument('-color', dest='color', help='color for points could to be compared to ground truth', default='b', type=str)

    args = parser.parse_args()

    return args

if __name__ == "__main__":

    options = parse_arguments()
    if options.results[-1] !='/':
        options.results += '/'
    os.chdir(options.results+'logs/')

    command_extract_id_pair = 'grep \"OPTIMIZE\" numsLog.txt > KFrameID'
    print('in folder:')
    os.system('pwd')
    print('run command: ', command_extract_id_pair)
    os.system(command_extract_id_pair)

    optimize_info = pd.read_csv('KFrameID', delim_whitespace=True, header = None, 
    names = ['OPT', 'nPoints', 'pts', 'nPlanes', 'pls', 'nRes', 'ac', 're', 'nLRes', 'li', 'res', 'newest', 'KID', 'RID', 'SID'])

    kf_rf_idpair = optimize_info[['KID', 'RID']]
    if (options.host == 0):
        rid = '0'
    else:
        rid_series = kf_rf_idpair.loc[kf_rf_idpair['KID'] == 'K'+str(options.host)+',', 'RID']

        rid_str = rid_series.values[0]
        rid = rid_str[1:-1]


    os.chdir('/media/amber/www/devel/dsop_ws/devel/lib/dso_plane_ros/scripts')
    print('in folder:')
    os.system('pwd')
    command_point_select_plot = './compare_point_depth.sh ' + options.results + ' ' + str(options.host) + ' ' + str(options.age) + ' ' + rid + ' ' + options.color
    print('run command: ', command_point_select_plot)
    os.system(command_point_select_plot)
    


