#!/usr/bin/env python

import sys
import rospy
from std_msgs.msg import String


class Dispatcher():
    def __init__(self):
        self.listCommands= []     # list of commands triggered by the analysis of the latest record of the session

        # initialize ROS node
        rospy.init_node('dispatcher', anonymous=True)
        # initialize publishers/subscribers
        # rospy.Subscriber([topic_name],[topic_type],[callback_function_name])
        rospy.Subscriber('irecheckcommand', String, self.commandCallback)
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])
        self.pubMsg = rospy.Publisher('robotcommand', String, queue_size=10) 

        # keep python from exiting until this node is stopped
        rospy.spin()

    
    # parse the command and call for the appropriate robot action
    def commandCallback(self, data):
        # log the reception of the message
        message = data.data
        rospy.loginfo(rospy.get_caller_id() + '- received %s', message)
        # split the message in the set of active commands
        self.listCommands = message.strip().split()
        # [DEBUG ONLY]
        print(self.listCommands)
        # issue the corresponding robot commands, in order of priority
        for idx, item in enumerate(self.listCommands):
            if item == "autoWIN":
                rospy.loginfo("robotWIN")
                self.pubMsg.publish("robotWIN")
            elif item == "autoLOSS":
                rospy.loginfo("robotLOSS")
                self.pubMsg.publish("robotLOSS")
            elif item == "nextGame":
                rospy.loginfo("nextGame " + self.listCommands[idx+1] + " " + self.listCommands[idx+2])
                self.pubMsg.publish("nextGame " + self.listCommands[idx+1] + " " + self.listCommands[idx+2])
            else:
                pass


#########################################################################
if __name__ == "__main__":
    try:
        myDispatcher = Dispatcher()
    except rospy.ROSInterruptException:
        pass
