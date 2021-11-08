#! /usr/bin/env python3

"""
Platforms package
Date: 2021/07/13
Author: Jianling ZOU 
"""

import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import copy
import os
import rospy
import random
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from qt_gesture_controller.srv import *
from qt_motors_controller.srv import *
from qt_behaviour_control.srv import *
from threading import Thread


class RobotBehavior(object):
	"""
	This classe has two functions which can read the behavior file and publish to speech, emotion and gesture topic.
	It should be used through the WOZ interface by using flask server.
	"""
	def __init__(self):
		rospy.init_node('behavior_control',anonymous=True)
		rospy.wait_for_service('/qt_robot/gesture/play')
		rospy.wait_for_service('/qt_robot/motors/home')
		# Name of gesture 
		self.gesture_name= ""
		# Speed of gesture
		self.speed = 0
		# list for emotions
		self.emotion = []
		# list for sentences of speech
		self.speech = []
		# first name of patient
		self.fname = "Thomas"   # here we need to change to a subscriber for patient's name
		# Create ROS topic publishers for emotion and speech
		self.speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
		self.emotion_pub = rospy.Publisher('/qt_robot/emotion/show',String, queue_size=10)

	def load_info(self,data):		
		"""
		Function for load infomation of behavior file. 
		It will get from the behavior file the name and speed of gesture, the sentences of speech and the name of emotion. 
		And it will save the first name of the patient	

		Args:
			self: The object pointer
			data: The button name
		"""
		# print (data)
		# print ("type: ", type(data))
		print ("Executing beahvior ", (data.data))
		# f = open("/home/qtrobot/catkin_ws/src/woz_interface/comportement/"+ data.Name +".txt", "r")  # you need to change the path here
		# f = open("/home/carnieto/catkin_ws/src/qt_behaviour_control/src/comportement/"+ data.data +".txt", "r")  # you need to change the path here
		f = open("~/catkin_ws/src/qt_behaviour_control/src/comportement/"+ data.data +".txt", "r")  # you need to change the path here
		# Save information
		# first line of file is infomation of gesture 
		line = f.readline()
		a=line.split(";")
		self.gesture_name = eval(a[0])
		self.speed = float(a[1])
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

		# Creat threads for gesture and speech + emotion
		t2=Thread(target=self.gesture_control,name="Gesture")
		t3=Thread(target=self.speech_emotion,name="SpeechEmotion")
		t2.start()
		t3.start()
		t2.join()
		t3.join()
		
		return True
	def listener(self):
		# Create a button name subscriber
		# Server = rospy.Service('/irecheck/buttonName', behavior_control, self.load_info) # Create Service Server
		rospy.Subscriber("/irecheck/button_name", String, self.load_info)
		rospy.spin()

	
	def gesture_control(self):
		"""
		Function for call Ros service that send gesture name and its speed.
	
		Args:
		self: The object pointer
		"""
		try:
			# call service of gesture with name and speed
			gesture_com = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
			res_gesture = gesture_com(self.gesture_name, self.speed)
			# go back to home pose
			home_pose = rospy.ServiceProxy('/qt_robot/motors/home',home)
			res_home = home_pose(['head','left_arm','right_arm'])
			# turn fail info when gesture can't be played
			if not res_gesture.status:
				print("Could not play gesture '%s'." % self.gesture_name)			
		except rospy.ServiceException as e:
			print("Service call failed: %s." % e)

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
				rospy.sleep(1) # for sychonize with the gesture
				self.emotion_pub.publish(self.emotion[0])
				self.speech_pub.publish(self.speech[0])
			else :
				i = random.randint(0,len(self.emotion)-1) # choose in random way the sentence of speech and the emotion
				rospy.sleep(1)
				self.emotion_pub.publish(self.emotion[i])
				self.speech_pub.publish(self.speech[i])
		except rospy.ServiceException as e:
			print("Service call failed: %s." % e)


if __name__ == "__main__":
	behavior = RobotBehavior()
	behavior.listener()



			
			

    

		
    
    
    
