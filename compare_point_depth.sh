
# Note: AGE input should be at least 1+HOST_ID, since it's the allKeyFramesHistory.size()-1, and points don't get activated on the lastest KFrame

# example script:
# ./compare_point_depth.sh ../results_dso_500_images/ 0 0 0 g pov /media/amber/www/data/ICL_living_room_traj0_frei_png/depth_pov
# ./compare_point_depth.sh ../results_dso_n500_images/ 0 0 0 g image /media/amber/www/data/ICL_living_room_traj0n_frei_png/depth

RESULTS_FOLDER=$1
HOST=$2
AGE=$3
PIC_ID=$4
COLOR=$5
GT_TYPE=$6 # pov is pov depth file, image is converted depth image
GT_PATH=$7
TRIAL=$8 # name template for output pcd file 


if [ ${#PIC_ID} -eq 1 ]
then
    PIC_IDD=000"$PIC_ID"
elif [ ${#PIC_ID} -eq 2 ]
then
    PIC_IDD=00"$PIC_ID"
elif [ ${#PIC_ID} -eq 3 ]
then
    PIC_IDD=0"$PIC_ID"
elif [ ${#PIC_ID} -eq 4 ]
then
    PIC_IDD=PIC_ID
fi



if [ $GT_TYPE == 'pov' ]
then
    echo reading from POV DEPTH file
    SCENE_DEPTH_FILE=scene_00_"$PIC_IDD".depth

    echo ./pcl_point_select "$GT_PATH"/"$SCENE_DEPTH_FILE" "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera gt_host"$HOST"_age"$AGE"_"$TRIAL".pcd pov gr

    ./pcl_point_select "$GT_PATH"/"$SCENE_DEPTH_FILE" "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera gt_host"$HOST"_age"$AGE"_"$TRIAL".pcd pov gr

    echo ./pcl_point_select "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera compare_host"$HOST"_age"$AGE"_"$TRIAL".pcd uvdepth "$COLOR"

    ./pcl_point_select "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera compare_host"$HOST"_age"$AGE"_"$TRIAL".pcd uvdepth "$COLOR"

    pcl_viewer gt_host"$HOST"_age"$AGE"_"$TRIAL".pcd -bc 1,1,1 -ps 10 -ax 1 compare_host"$HOST"_age"$AGE"_"$TRIAL".pcd -ps 10 


elif [ $GT_TYPE == 'image' ]
then
    echo reading from DEPTH IMAGE file
    DEPTHIMAGE_FILE=0"$PIC_IDD".png

    echo ./pcl_point_select "$GT_PATH"/"$DEPTHIMAGE_FILE" "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera gt_host"$HOST"_age"$AGE"_"$TRIAL".pcd image gr

    ./pcl_point_select "$GT_PATH"/"$DEPTHIMAGE_FILE" "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera gt_host"$HOST"_age"$AGE"_"$TRIAL".pcd image gr

    echo ./pcl_point_select "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera compare_host"$HOST"_age"$AGE"_"$TRIAL".pcd uvdepth "$COLOR"

    ./pcl_point_select "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera compare_host"$HOST"_age"$AGE"_"$TRIAL".pcd uvdepth "$COLOR"

    pcl_viewer gt_host"$HOST"_age"$AGE"_"$TRIAL".pcd -bc 1,1,1 -ps 10 -ax 1 compare_host"$HOST"_age"$AGE"_"$TRIAL".pcd -ps 10
    

fi

    

