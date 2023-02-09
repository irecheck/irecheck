#!/usr/bin/env python3

import rospy
import smach
import pandas as pd
import random
import roslib; roslib.load_manifest('smach')
from std_msgs.msg import String
from qt_nuitrack_app.msg import *
from datetime import datetime
#!/usr/bin/env python
import rospy
from qt_robot_interface.srv import *
# from qt_nuitrack_app.msg import Gestures

# possibilities = ['Hello!', 'How are you?', 'Hey, friend!', 'Aloha', "Hey There!", "Hi!"]

possibilities = ['Bonjour!', 'Alo', 'Hey, monami!', 'Coucou!', "Ça va?", "Venis!", 'Est que tu veux jouer avec moi?']




class Demo():
    def __init__(self):
        
        rospy.init_node('SRD_Demo', anonymous=True)
        # initialize ROS node
        # initialize subscribers
        rospy.Subscriber('/qt_nuitrack_app/faces', Faces, self.nuitrackCallback)
        # rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        # rospy.Subscriber('autodecisions', String, self.decisionsCallback)
        # self.gesture = rospy.ServiceProxy('/qt_robot/gesture/play', 'gesture_play')
        self.speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        # self.pubMsg = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
        self.gesture = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)

        self.gesture.publish("QT/Dance/Dance-1-3")
        self.gesture.publish("bye")
        rospy.loginfo("WORKING!")
        rospy.spin()


    def nuitrackCallback(self, msg):
        
        x = random.randint(1, 4)
        y = random.randint(1, 4)
        dance = "QT/Dance/Dance-"+ str(x) + "-" + str(y)
        rospy.loginfo("Dance: " + dance)
        
        say = random.choice(possibilities)
        # self.gesture.publish("QT/bye")
        self.gesture.publish(dance)
        rospy.loginfo(say)
        #self.speechSay(say)
       
       
        #self.speechSay('Hello!')
        #self.pubMsg.publish('How are you?')
        
        rospy.sleep(10)









#########################################################################
if __name__ == "__main__":
    try:
        demo = Demo()
    except rospy.ROSInterruptException:
        pass






# Gestures message structure
# qt_nuitrack_app/GestureInfo[] gestures
#     int32 id
#     string name

def gesture_callback(msg):
    rospy.loginfo(msg)

def listener():
    gesture_sub = rospy.Subscriber('/qt_nuitrack_app/gestures', Gestures, gesture_callback)

# if __name__ == '__main__':
#     # In ROS, nodes are uniquely named. If two nodes with the same
#     # name are launched, the previous one is kicked off. The
#     # anonymous=True flag means that rospy will choose a unique
#     # name for our 'listener' node so that multiple listeners can
#     # run simultaneously.
#     rospy.init_node('listener', anonymous=True)
#     listener()
#     try:
#         # spin() simply keeps python from exiting until this node is stopped
#         rospy.spin()
#     except KeyboardInterrupt:
#         print("Shutting down")