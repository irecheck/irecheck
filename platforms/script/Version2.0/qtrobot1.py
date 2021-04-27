#! /usr/bin/env python3
# -*- coding: latin-1 -*-

"""
Platforms package
Date: 2020/12/04
Author: Jianling ZOU 
"""

import copy
import rospy
import random
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from qt_gesture_controller.srv import *
from qt_motors_controller.srv import *
from threading import Thread


class RobotBehavior(object):
	"""
	This classe has two functions which can read the behavior file and publish to speech, emotion and gesture topic.
	It should be used through the WOZ interface by using flask server.
	"""
	
	def load_info(self,name,fname,lname,fname2):		
		"""
		Function for load infomation of behavior file. 
		It will get from the behavior file the name and speed of gesture, the sentences of speech and the name of emotion. 
		And it will save the first name of the patient	

		Args:
			self: The object pointer
			name(str): The name of behavior file
			fname(str): fname The first name of patient	
			lname(str): lname The last name of patient
		"""
		# Name of gesture 
		self.gesture_name= ""
		# Speed of gesture
		self.speed = 0
		# list for emotions
		self.emotion = []
		# list for sentences of speech
		self.speech = []
		# first name of patient
		self.fname = ""
		self.fname2 = ""
		#global Fname # global variable, the first name of patient
		self.fname = fname
		self.fname2 = fname2
		# import the file of behaviours
		f = open("/home/jennie/irecheck_ws/src/irecheck/platforms/comportement/"+name+".txt", "r") 
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
		t2=Thread(target=self.gesture_control,name="Gesture")
		t3=Thread(target=self.speech_emotion,name="SpeechEmotion")
		t2.start()
		t3.start()
		t2.join()
		t3.join()

	
	
	def gesture_control(self):
		"""
		Function for publish information that we get from the load_info function.
		If there are more than one choice of speech and emotion, it will choose one of them by random way
	
		Args:
		self: The object pointer
		say(ros publisher): The Publisher of rostopic "/qt_robot/speech/say"
		emo(ros publisher): The Publisher of rostopic "/qt_robot/emotion/play"
		"""
		# command emotion, speech and gesture 
		try:
			rospy.wait_for_service('/qt_robot/gesture/play')
			rospy.wait_for_service('/qt_robot/motors/home')
			# call service of gesture with name and speed
			gesture_com = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
			res_gesture = gesture_com(self.gesture_name, self.speed)
			# go back to home pose
			home_pose = rospy.ServiceProxy('/qt_robot/motors/home',home)
			res_home = home_pose(['head','left_arm','right_arm'])
			if not res_gesture.status:
				print("Could not play gesture '%s'." % self.gesture_name)			
		except rospy.ServiceException as e:
			print("Service call failed: %s." % e)

	def speech_emotion(self):
		say = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
		emo = rospy.Publisher('/qt_robot/emotion/show',String, queue_size=10)
		try:
			if len(self.emotion) == 1:
				rospy.sleep(1) # for sychonize with the gesture
				emo.publish(self.emotion[0])
				say.publish(self.speech[0])
			else :
				i = random.randint(0,len(self.emotion)-1) # choose in random way the sentence of speech and the emotion
				rospy.sleep(1)
				emo.publish(self.emotion[i])
				say.publish(self.speech[i])
		except rospy.ServiceException as e:
			print("Service call failed: %s." % e)
			
			

    

		
    
    
    
