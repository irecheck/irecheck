#!/usr/bin/env python

import os
import sys
import rosbag
import numpy as np
import rospy
from datetime import datetime
from qt_nuitrack_app.msg import *
import pandas as pd
from std_msgs.msg import String
import time
#from sensor_msgs.msg import CameraInfo



class Camera_class():

    def __init__(self):

        # initialize ROS node
        rospy.init_node('Robot_camera_posture', anonymous=True)
        # subscribed topic 
        rospy.Subscriber('qt_nuitrack_app/skeletons', Skeletons, self.nuitrackCallback)
        
        # topic where we publish
        self.dist_pub = rospy.Publisher("distances", String, queue_size = 10)

        
        # print('Finished init')

    def nuitrackCallback(self, ros_data):
        #print('ok')
        distR = 0
        distL = 0

        shJR = [0,0,0]
        shJL = [0,0,0]
        
        shR = 12
        shL = 6
        if ros_data.skeletons[0].joints[1].confidence>.7:
            head = ros_data.skeletons[0].joints[1].real

            if ros_data.skeletons[0].joints[15].confidence>.7:
                Rhand = ros_data.skeletons[0].joints[15].real
        #print(Rhand[0])
                distR=np.sqrt((head[0]-Rhand[0])*(head[0]-Rhand[0]) + (head[1]-Rhand[1])*(head[1]-Rhand[1]) +(head[2]-Rhand[2])*(head[2]-Rhand[2]))
                distR=int(np.round(distR))
                #print(distR)

            if ros_data.skeletons[0].joints[9].confidence>.7:
                Lhand = ros_data.skeletons[0].joints[9].real
                distL=np.sqrt((head[0]-Lhand[0])*(head[0]-Lhand[0]) + (head[1]-Lhand[1])*(head[1]-Lhand[1]) +(head[2]-Lhand[2])*(head[2]-Lhand[2]))
                distL=int(np.round(distL))
                
        if ros_data.skeletons[0].joints[shR].confidence>.7:
            shJR = ros_data.skeletons[0].joints[shR].real
            
        if ros_data.skeletons[0].joints[shL].confidence>.7:
            shJL = ros_data.skeletons[0].joints[shL].real
        
        hour = datetime.now()
        #if distR + distL > 1:
            #output_string = "{{'R_dist': {}, 'L_dist': {} }}".format(str(distR), str(distR))
        output_string = "{{'Time': {}, 'R_dist': {}, 'L_dist': {} , 'x_R_sh': {}, 'y_R_sh': {}, 'z_R_sh': {},  'x_L_sh': {}, 'y_L_sh': {}, 'z_L_sh': {} }}".format(str(hour),str(distR), str(distR), str(shJR[0]),str(shJR[1]), str(shJR[2]), str(shJL[0]),str(shJL[1]), str(shJL[2]))
            
        # print(output_string)
            
        self.dist_pub.publish(output_string)
	
        
        
if __name__ == '__main__':
    try:
        myCamera = Camera_class()
        print('Working!')
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    
