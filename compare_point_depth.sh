
# Note: AGE input should be at least 1+HOST_ID, since it's the allKeyFramesHistory.size()-1, and points don't get activated on the lastest KFrame

# example script:
# ./compare_point_depth.sh ../results_dsop10_500_images/ 0 0 0 g
# ./compare_point_depth.sh ../results_dso_500_images/ 1 2 51 b

RESULTS_FOLDER=$1
HOST=$2
AGE=$3
PIC_ID=$4
COLOR=$5



if [ ${#PIC_ID} -eq 1 ]
then
    SCENE_DEPTH_FILE=scene_00_000"$PIC_ID".depth
elif [ ${#PIC_ID} -eq 2 ]
then
    SCENE_DEPTH_FILE=scene_00_00"$PIC_ID".depth
elif [ ${#PIC_ID} -eq 3 ]
then
    SCENE_DEPTH_FILE=scene_00_0"$PIC_ID".depth
elif [ ${#PIC_ID} -eq 4 ]
then
    SCENE_DEPTH_FILE=scene_00_"$PIC_ID".depth
fi
    
echo ./pcl_point_select /media/amber/www/data/ICL_living_room_traj0_frei_png/depth_pov/"$SCENE_DEPTH_FILE" "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera gt_"$HOST".pcd pov gr

./pcl_point_select /media/amber/www/data/ICL_living_room_traj0_frei_png/depth_pov/"$SCENE_DEPTH_FILE" "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera gt_"$HOST".pcd pov gr

echo ./pcl_point_select "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera compare_"$HOST".pcd uvdepth "$COLOR"

./pcl_point_select "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".uvdepth "$RESULTS_FOLDER"host"$HOST"_age"$AGE".camera compare_"$HOST".pcd uvdepth "$COLOR"

pcl_viewer gt_"$HOST".pcd -bc 1,1,1 -ps 10 -ax 1 compare_"$HOST".pcd -ps 10 

