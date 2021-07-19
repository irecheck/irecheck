# !/bin/bash

source /home/qtrobot/robot/autostart/qt_robot.inc

SCRIPT_NAME="start_woz_interface"
LOG_FILE=$(prepare_logfile "$SCRIPT_NAME")

{
prepare_ros_environment
wait_for_ros_node "/rosout" 60
wait_for_ros_topic "/qt_robot/emotion/show" 60
wait_for_ros_topic "/qt_robot/gesture/play" 60
wait_for_ros_topic "/qt_robot/speech/say" 60

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
roslaunch woz_interface woz_interface.launch
} &>> ${LOG_FILE}

