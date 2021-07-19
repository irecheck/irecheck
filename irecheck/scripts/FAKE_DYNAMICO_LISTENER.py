#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

# publish fake dynamicomsg with a fixed frequency
def talker():
    toggle = 0
    pub = rospy.Publisher('dynamicomsg', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
        if (toggle == 0):
            hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"2021-6-3 9:56:10","score":32,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'
            toggle =1
        else:
            hello_str = '[{"updatedAt":1621435616565,"countryCode":"FR","avatar":"default","birthMonth":9,"birthYear":2007,"createdAt":"2021-5-19 14:46:56","handedness":"left","userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","gender":"female","languageCode":"EN","displayName":"Girl left."}]'
            toggle = 0
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

# publish ONE dynamicomsg
def talkerOnce():
    toggle = 0
    pub = rospy.Publisher('dynamicomsg', String, queue_size=10)
    rospy.init_node('talkerOnce', anonymous=True)
    hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"2021-6-3 9:56:10","score":32,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'
    rospy.loginfo(hello_str)
    pub.publish(hello_str)

if __name__ == '__main__':
    try:
        talkerOnce()
    except rospy.ROSInterruptException:
        pass