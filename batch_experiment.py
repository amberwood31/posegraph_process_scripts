import os



trials = 5
results_folder_template = 'results_newdsop_living_traj0_trial'
output_folder_name_templete = 'nplanes5_'

dso_filenames = ['sim_living_traj0', 'sim_living_traj0', 'sim_living_traj1','sim_living_traj1', 'sim_living_traj2','sim_living_traj2', 'sim_living_traj3', 'sim_living_traj3', 'sim_office_traj0', 'sim_office_traj0',  'sim_office_traj1', 'sim_office_traj1', 'sim_office_traj2', 'sim_office_traj2', 'sim_office_traj3', 'sim_office_traj3']


input_filenames = ['living_room_traj0', 'living_room_traj0', 'living_room_traj1', 'living_room_traj1', 'living_room_traj2', 'living_room_traj2', 'living_room_traj3', 'living_room_traj3', 'office_room_traj0', 'office_room_traj0', 'office_room_traj1','office_room_traj1', 'office_room_traj2', 'office_room_traj2', 'office_room_traj3', 'office_room_traj3']

gt_path = ['gt_icl_' + name for name in input_filenames]


if __name__ == "__main__":

    os.chdir('/media/amber/www/devel/dsop_ws/devel/lib/dso_plane_ros')


    run_command = []
    output_path = []
    for i in range(0, len(input_filenames)):

        input_template = input_filenames[i]
        command = 'rosrun dso_plane_ros dso_plane_ros_imagefile files=/media/amber/www/data/ICL_' + input_template +'_frei_png/rgb calib=/media/amber/www/data/ICL_' + input_template + '_frei_png/camera.txt mode=2 plane=1 nogui=1 nomt=1 planeActive=5'
            
        path = output_folder_name_templete + 'results_newdsop_' + input_template

        if i%2 == 1:
            command = command + ' reverse=1'
            path = path + '_reverse'

        run_command.append(command)
        output_path.append(path)

    # print(run_command)
    # print(output_path)

    for j in range(0, len(input_filenames)):

        for i in range(0, trials):
            # run experiment
            os.system(run_command[j])

            # create experimental results folder
            results_folder_name = output_path[j] + '_trial' + str(i)
            mkdir_command = 'mkdir '+ results_folder_name
            os.system(mkdir_command)

            # move results
            os.system('./move_results_to_folder.sh ' + results_folder_name)



    # os.chdir('/media/amber/www/devel/dsop_ws/devel/lib/dso_plane_ros/scripts')