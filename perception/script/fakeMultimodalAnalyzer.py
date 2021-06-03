#!/usr/bin/env python
 
import sys
import rospy
from std_msgs.msg import String
from irecheck.srv import MMAFieldsSrv,MMAFieldsSrvResponse


class FakeMultimodalAnalyzer():
    def __init__(self):
        # initialize ROS node
        rospy.init_node('fakemultimodalanalyzer', anonymous=True)
        # initialize publishers/subscribers
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])
        self.pubMsg = rospy.Publisher('multimodalmsg', String, queue_size=10)
        # rospy.Subscriber([topic_name],[topic_type],[callback_function_name])
        # initialize services (server)
        # rospy.Service([service_name],[service_type],[handler])
        self.servFields = rospy.Service('sendMMAFields', MMAFieldsSrv, self.sendMMAFieldsHandler)
        rospy.loginfo("Started sendMMAFields service")

        # display usage instructions
        print("\n\nThis is the Multimodal Analyzer simulator. Provide info in the following format:")
        print("***REMOVED***lying, sitting, standing***REMOVED*** ***REMOVED***happy, sad, neutral***REMOVED***")
        print("e.g.: sitting happy")
        print("Send as many info records as you want and use CTRL+C to quit.")

    
    # handler for the service of sending the MMA field names
    def sendMMAFieldsHandler(self, req):
        ros_response = "Posture Emotion"
        response = MMAFieldsSrvResponse()
        response.fields = ros_response
        return response


    # get fake behavioural info and publish them as a ROS message
    def getData(self):
        ros_message = raw_input()

        # check message content existence before publication
        if (ros_message != ""):
            rospy.loginfo(ros_message)
            self.pubMsg.publish(ros_message)


#########################################################################
if __name__ == '__main__':
    myFakeMultimodalAnalyzer = FakeMultimodalAnalyzer()
    while not rospy.is_shutdown():
        myFakeMultimodalAnalyzer.getData()