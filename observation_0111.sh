
#for noiseless data

python visualize_comparison_point_depth.py -results ../results_dsop10_500_images/ -host 20 -age 21 -color b -gt_type pov -gt_path /media/amber/www/data/ICL_living_room_traj0_frei_png/depth_pov -pcd_name noiseless

python visualize_comparison_point_depth.py -results ../results_dsop10_500_images/ -host 20 -age 23 -color g -gt_type pov -gt_path /media/amber/www/data/ICL_living_room_traj0_frei_png/depth_pov -pcd_name noiseless

pcl_viewer gt_host20_age21_noiseless.pcd -bc 1,1,1 -ps 10 -ax 1 compare_host20_age21_noiseless.pcd -ps 10 compare_host20_age23_noiseless.pcd -ps 10


#for noisy data

python visualize_comparison_point_depth.py -results ../results_dsop_n500_images/ -host 20 -age 21 -color b -gt_type image -gt_path /media/amber/www/data/ICL_living_room_traj0n_frei_png/depth -pcd_name noisy

python visualize_comparison_point_depth.py -results ../results_dsop_n500_images/ -host 20 -age 23 -color g -gt_type image -gt_path /media/amber/www/data/ICL_living_room_traj0n_frei_png/depth -pcd_name noisy

pcl_viewer gt_host20_age21_noisy.pcd -bc 1,1,1 -ps 10 -ax 1 compare_host20_age21_noisy.pcd -ps 10 compare_host20_age23_noisy.pcd -ps 10



