import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

from batch_eth_experiment import input_filenames

rmse_file1 = sys.argv[1]
rmse_file2 = sys.argv[2]
scale_file1 = sys.argv[3]
scale_file2 = sys.argv[4]
name_template = ''
if len(sys.argv)>5:
    name_template = sys.argv[5]
plot_filename = name_template + '_accumulative_plot'
# threshold = sys.argv[2]
rmse_results1 = pd.read_csv(rmse_file1, sep = ',', header = 0, index_col=0)
rmse_results2 = pd.read_csv(rmse_file2, sep = ',', header = 0, index_col=0)
# print(rmse_results)

# print(rmse_results.le(float(threshold)))
# print(rmse_results.le(float(threshold)).sum().sum())
print('mean dso rmse: ')
print(rmse_results1.median())
print('mean dsop rmse: ')
print(rmse_results2.median())

scale_results1 = pd.read_csv(scale_file1, sep = ',', header = 0, index_col=0)
scale_results2 = pd.read_csv(scale_file2, sep = ',', header = 0, index_col=0)
# print(rmse_results)

# print(rmse_results.le(float(threshold)))
# print(rmse_results.le(float(threshold)).sum().sum())
print('mean dso scale: ')
print(scale_results1.median())
print('mean dsop scale: ')
print(scale_results2.median())



# for i in range(0, len(input_filenames)):
#     print('dataset: ', input_filenames[i])

#     if i%2 == 1:
#         print('reverse')


