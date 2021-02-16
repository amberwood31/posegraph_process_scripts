import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

from batch_experiment import dso_filenames

rmse_file1 = sys.argv[1]
rmse_file2 = sys.argv[2]
name_template = ''
if len(sys.argv)>3:
    name_template = sys.argv[3]
plot_filename = name_template + '_accumulative_plot'
# threshold = sys.argv[2]
rmse_results1 = pd.read_csv(rmse_file1, sep = ',', header = 0, names = dso_filenames)
rmse_results2 = pd.read_csv(rmse_file2, sep = ',', header = 0, names = dso_filenames)
# print(rmse_results)

# print(rmse_results.le(float(threshold)))
# print(rmse_results.le(float(threshold)).sum().sum())
print(rmse_results1[0:5])

accumulative_counts1 = []
accumulative_counts2 = []
thresholds_range = np.arange(0,0.42,0.01)

# selected_option = [0,2,4,6,8,10,12,14]
selected_option = range(0,rmse_results1.shape[1])
for threshold in thresholds_range:
    count1 = rmse_results1.iloc[:,selected_option].le(float(threshold)).sum().sum()
    accumulative_counts1.append(count1/2)

    count2 = rmse_results2.iloc[:,selected_option].le(float(threshold)).sum().sum()
    accumulative_counts2.append(count2/2)

fig, ax = plt.subplots()
plt.plot(thresholds_range, accumulative_counts1,  'b')
plt.plot(thresholds_range, accumulative_counts2,  '-r*')
print('saving plots to ', plot_filename)
plt.savefig(plot_filename)
plt.show()


