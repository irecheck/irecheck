#! /usr/bin/env python2.7

"""
Platforms package
Date: 2021/07/13
Author: Jianling ZOU 
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import copy
import rospy
import random
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import Int32
#from qt_gesture_controller.srv import *
from qt_motors_controller.srv import *
#from qt_behaviour_control.srv import *
#from threading import Thread


class RobotBehavior(object):
	"""
	This classe has two functions which can read the behavior file and publish to speech, emotion and gesture topic.
	It should be used through the WOZ interface by using flask server.
	"""
	def __init__(self):
		rospy.init_node('behavior_control',anonymous=True)
		rospy.wait_for_service('/qt_robot/motors/home')
		# Name of gesture 
		self.gesture_name= ""
		# list for emotions
		self.emotion = []
		# list for sentences of speech
		self.speech = []
		# first name of patient
		self.fname = "Thomas"   # here we need to change to a subscriber for patient's name
		# Create ROS topic publishers for emotion and speech and gesture
		self.speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
		self.emotion_pub = rospy.Publisher('/qt_robot/emotion/show',String, queue_size=10)
		self.gesture_pub = rospy.Publisher('/qt_robot/gesture/play',String,queue_size=10)

	def load_info(self,data):		
		"""
		Function for load infomation of behavior file. 
		It will get from the behavior file the name and speed of gesture, the sentences of speech and the name of emotion. 
		And it will save the first name of the patient	

		Args:
			self: The object pointer
			data: The button name
		"""

		f = open("/home/qtrobot/catkin_ws/src/woz_interface/comportement/"+ data.data +".txt", "r")  # you need to change the path here
		# Save information
		# first line of file is infomation of gesture 
		line = f.readline()
		a=line.split(";")
		self.gesture_name = eval(a[0])
		# next lines are info of speech, emotion 
		line = f.readline()
		# save information of emotions and speech
		while line:
			a = line.split(";")
			self.emotion.append(eval(a[0]))
			self.speech.append(eval(a[1]))	
			line = f.readline()
		# close the file
		f.close()

		#return True

	def listener(self):
		# Create a button name subscriber
		#Server = rospy.Service('/irecheck/buttonName', behavior_control, self.load_info) # Create Service Server
		rospy.Subscriber("/irecheck/button_name", String, self.load_info)
		rospy.spin()

	def speech_emotion(self):
		"""
		Function for publish information that we get from the load_info function.
		If there are more than one choice of speech and emotion, it will choose one of them by random way
	
		Args:
		self: The object pointer
		"""
		# command emotion, speech
		try:
			if len(self.emotion) == 1:
				#rospy.sleep(1) # for sychonize with the gesture
				self.emotion_pub.publish(self.emotion[0])
				self.speech_pub.publish(self.speech[0])
				self.gesture_pub.publish(self.gesture_name)
				# go back to home pose
				home_pose = rospy.ServiceProxy('/qt_robot/motors/home',home)
				res_home = home_pose(['head','left_arm','right_arm'])
			else :
				i = random.randint(0,len(self.emotion)-1) # choose in random way the sentence of speech and the emotion
				#rospy.sleep(1)
				self.emotion_pub.publish(self.emotion[i])
				self.speech_pub.publish(self.speech[i])
				self.gesture_pub.publish(self.gesture_name)
				# go back to home pose
				home_pose = rospy.ServiceProxy('/qt_robot/motors/home',home)
				res_home = home_pose(['head','left_arm','right_arm'])
		except rospy.ServiceException as e:
			print("Service call failed: %s." % e)


if __name__ == "__main__":
	behavior = RobotBehavior()
	behavior.listener()



			
			

    

		
    
    
    
