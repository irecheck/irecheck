#!/usr/bin/env python3

# from datetime import time
import time

from numpy import record
import rospy
from std_msgs.msg import String
import pandas as pd


class FakeDynamico():

    def __init__(self):
        rospy.init_node('talker', anonymous=True)
        self.pub = rospy.Publisher('dynamicomsg', String, queue_size=10)
        self.dataframe = pd.read_csv("/home/carnieto/Documents/iReCHeCk_logs/14_Sep/14-09-2021_16-02-44.csv")
        # print(self.dataframe)
        self.id = 0

    # publish fake dynamicomsg with a fixed frequency
    def talker(self):
        toggle = 0
        rate = rospy.Rate(1) # 1hz
        typed = ''
        while 1:
            # if (toggle == 0):
        
            typed = input("Just press enter:")
            
            if typed == 'q':
                break
            
            try:
            # hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"%s","score":72,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'%(time.time())
                line = self.dataframe.iloc[self.id].to_json()
            except:
                rospy.loginfo("Dataframe is over!")
                break

            # print("LINEE", line)
            
            # hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"%s","score":72,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'%(time.time())
            hello_str = '[%s]'%(line)
                    # toggle =1
                # else:
                    # hello_str = '[{"updatedAt":1621435616565,"countryCode":"FR","avatar":"default","birthMonth":9,"birthYear":2007,"createdAt":"2021-5-19 14:46:56","handedness":"left","userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","gender":"female","languageCode":"EN","displayName":"Girl left."}]'
                    # toggle = 0
            rospy.loginfo("Publishing  " + hello_str)
            self.pub.publish(hello_str)
            
            self.id += 1
            
    # publish ONE dynamicomsg
    def talkerOnce(self):
        toggle = 0
        # rospy.init_node('talkerOnce', anonymous=True)
        # pub = rospy.Publisher('dynamicomsg', String, queue_size=10)
        hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"2021-6-3 9:56:10","score":72,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'
        rospy.loginfo(hello_str)
        pub.publish(hello_str)

if __name__ == '__main__':
    try:
        fd = FakeDynamico()
        fd.talker()
        # talkerOnce()
        # talker()
    except rospy.ROSInterruptException:
        pass