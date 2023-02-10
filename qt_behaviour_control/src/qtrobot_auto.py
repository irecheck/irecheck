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
		# self.gesture_name= ""
		self.gesture_name= {}
		# list for emotions
		self.emotion ={}
		# list for sentences of speech
		self.speech = {}
		
		# time for the speech to wait to run to synchronize with gesture and emotion
		self.sync_time = 0 #in seconds

		# first name of patient
		# self.fname = "Thomas"   # here we need to change to a subscriber for patient's name
		self.fname =  str(sys.argv[1])  # here we need to change to a subscriber for patient's name
		self.fname2 =  str(sys.argv[2])  # here we need to change to a subscriber for patient's name
		
		# Create ROS topic publishers for emotion and speech and gesture
		self.speech_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
		self.emotion_pub = rospy.Publisher('/qt_robot/emotion/show',String, queue_size=10)
		self.gesture_pub = rospy.Publisher('/qt_robot/gesture/play',String,queue_size=10)

		print("Initiating the behavior for child <{}> and therapist <{}>".format(self.fname,self.fname2))

		# print "\n\nInitializing behavior handler!"
		# print 'Child name:', self.fname
		# print 'Therapist name:', self.fname2

		# print "\nLoading behavior from files"
		self.load_files()
		# print "\n\nDone! Script is ready and waiting for requests to run the behavior :D \n"
		# print "--"



	def load_info(self,data):		
		"""
		Function for load infomation of behavior file. 
		It will get from the behavior file the name and speed of gesture, the sentences of speech and the name of emotion. 
		And it will save the first name of the patient	

		Args:
			self: The object pointer
			data: The button name
		"""

		print ("Data:", data.data)

		# f = open("/home/qtrobot/catkin_ws/src/woz_interface/comportement/"+ data.data +".txt", "r")  # you need to change the path here
		# # Save information
		# # first line of file is infomation of gesture 
		# line = f.readline()
		# a=line.split(";")
		# self.gesture_name = eval(a[0])
		# # next lines are info of speech, emotion 
		# line = f.readline()
		# # save information of emotions and speech
		# while line:
		# 	a = line.split(";")
		# 	self.emotion.append(eval(a[0]))
		# 	self.speech.append(eval(a[1]))	
		# 	line = f.readline()
		# # close the file
		# f.close()
		self.speech_emotion()
		#return True




	def load_files(self):
		"""
		Function for load the files with the used behavior. 
		 
		Args:
			self: The object pointer
		
		"""

		# Jianling
		# files_path =  "/home/qtrobot/catkin_ws/src/woz_interface/comportement/"
		
		# My version
		home_path = os.path.expanduser("~")
		# files_path =  "/home/carnieto/catkin_ws/src/irecheck/qt_behaviour_control/src/comportement/"
		files_path =  "/home/carnieto/catkin_ws/src/irecheck/qt_behaviour_control/src/comportement_english/"
		
		
		for file_name in os.listdir(files_path):
			file_name=file_name.rsplit('.', 1)[0]
			# print "FILE NAME: ", file_name
			
			# return
			f = open( files_path + file_name +".txt", "r")  # you need to change the path here
			# f = open("/home/qtrobot/catkin_ws/src/woz_interface/comportement/"+ file_name +".txt", "r")  # you need to change the path here
			# Save information
			# first line of file is infomation of gesture 
			line = f.readline()
			a=line.split(";")
			
			self.gesture_name[file_name] = eval(a[0])
			# next lines are info of speech, emotion 
			line = f.readline()
			
			emotion_options = []
			speech_options = []
			# save information of emotions and speech
			while line:
				a = line.split(";")
				emotion_options.append(eval(a[0]))
				speech_options.append(eval(a[1]))	
				line = f.readline()
			
			self.emotion[file_name] = emotion_options
			self.speech[file_name] = speech_options
		
			# close the file
			f.close()

		# print "Loaded ", len(self.speech) ," files of behavior"

		#--- End of for
		
		# print "Printing Dictionaries"

		# print "\nGesture:"
		# print self.gesture_name

		# print "\nEmo:"
		# print self.emotion

		# print "\nSpecch:"
		# print self.speech


		# return 

		




	def speech_emotion(self, data):
		"""
		Function for publish information that we get from the load_info function.
		If there are more than one choice of speech and emotion, it will choose one of them by random way
	
		Args:
		self: The object pointer
		"""

		behavior_type = data.data

		# print "Executing behavior type: ", behavior_type

		# command emotion, speech
		try:
			if len(self.emotion[behavior_type]) == 1:
				i=0
				#rospy.sleep(1) # for sychonize with the gesture
				# self.emotion_pub.publish(self.emotion[behavior_type][0])
				# self.gesture_pub.publish(self.gesture_name[behavior_type])
				# rospy.sleep(self.sync_time)

				# self.speech_pub.publish(self.speech[behavior_type][0])
				# rospy.sleep(5)


				# # print("RESULT 1:", self.speech[behavior_type][0])
				# # go back to home pose
				# home_pose = rospy.ServiceProxy('/qt_robot/motors/home',home)
				# res_home = home_pose(['head','left_arm','right_arm'])
			else :
				i = random.randint(0,len(self.emotion[behavior_type])-1) # choose in random way the sentence of speech and the emotion
				#rospy.sleep(1)
			
			self.emotion_pub.publish(self.emotion[behavior_type][i])
			self.speech_pub.publish(self.speech[behavior_type][i])
			# rospy.sleep(5)
			# self.gesture_pub.publish(self.gesture_name[behavior_type][i])

			print ("AQUI", self.gesture_name[behavior_type])
			self.gesture_pub.publish(self.gesture_name[behavior_type])
			

			# gesture_com = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
			# res_gesture = gesture_com(self.gesture_name[i], 1)
			# res_gesture = gesture_com(self.gesture_name, self.speed)


			# gesture = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
			# gesture_exec = gesture('adieu',1)
			
			# print "Gesture flag", gesture_exec

			# rospy.sleep(self.sync_time)
			
			# print("RESULT <", i, ":>", self.speech[behavior_type][i])
			# go back to home pose
			# print "Calling the function home"
			home_pose = rospy.ServiceProxy('/qt_robot/motors/home',home)
			res_home = home_pose(['head','left_arm','right_arm'])
			
			# print "RES_HOME", res_home

		except rospy.ServiceException as e:
			print("Service call failed: %s." % e)


		# print ("VARIABLES")
		# print ("Speech: ",  self.speech)
		# print ("Emotion: ", self.emotion)
		# print ("Gesture: ", self.gesture_name)
		# print ("\n\n")

		# self.speech = []
		# self.emotion = []
		# self.gesture_name = []



	def listener(self):
		# Create a button name subscriber
		#Server = rospy.Service('/irecheck/buttonName', behavior_control, self.load_info) # Create Service Server
		rospy.Subscriber("/irecheck/button_name", String, self.speech_emotion)
		rospy.spin()

if __name__ == "__main__":
	behavior = RobotBehavior()
	behavior.listener()



			
			

    

		
    
    
    
