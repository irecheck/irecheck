#! /usr/bin/env python

##@package Platforms
#This package contains all programmes related to QTrobot, including behavior control, TF recognition.

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
from comportement_control.msg import GestureCommand

Fname = ""


##  This classe has two functions which can read the behavior file and publish to speech, emotion and gesture topic.
# It should be used through the WOZ interface by using flask server.

class RobotBehavior(object):

	## Name of gesture 
	self.gesture_name= ""
	## Speed of gesture
	self.speed = 0
	## list for emotions
	self.emotion = []
	## list for sentences of speech
	self.speech = []


	## Function for load infomation of behavior file. 
	# It will get from the behavior file the name and speed of gesture, the sentences of speech and the name of emotion. 
	# And it will save the first name of the patient	
	# @param self The object pointer
	# @param name The name of behavior file
	# @param fname The first name of patient	
	def load_info(self,name,fname):		
		global Fname # global variable, the first name of patient
		Fname = fname
		# import the file of behaviours
		f = open("/home/jennie/irecheck/iReCheck/QT_ws/src/comportement_control/comportement/"+name+".txt", "r")
		line = f.readline()
		a=line.split(";") 
		# Save information
		# first line of file is infomation of gesture 
		self.gesture_name = a[0]
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

	## Function for publish information that we get from the load_info function.
	# If there are more than one choice of speech and emotion, it will choose one of them by random way
	# @param self The object pointer
	# @param say The Publisher of rostopic "/qt_robot/speech/say"
	# @param emo The Publisher of rostopic "/qt_robot/emotion/play"
	# @param gesture The Publisher of rostopic "comportement/gesture_name"
	
	def realisation(self,say,emo,gesture):
		
		# initialisation of gesture
		target_gesture = GestureCommand() # The type of this variable is GestureCommand which contains the name and the speed of gesture  
		# command gesture
		target_gesture.name = self.gesture_name
		target_gesture.speed = self.speed
		gesture.publish(target_gesture)

		# command emotion and speech
		if len(self.emotion) == 1:
			rospy.sleep(2) # for sychonize with the gesture
			emo.publish(self.emotion[0])
			say.publish(self.speech[0])
		else :
			i = random.randint(0,len(self.emotion)-1) # choose in random way the sentence of speech and the emotion
			rospy.sleep(2)
			emo.publish(self.emotion[i])
			say.publish(self.speech[i])


			
			
			

#if __name__ == "__main__":
    

    #this is the function for test the programme without WOZ interface
    
    # behaviour command
    # rospy.init_node('behaviour_command', anonymous=True)
    # creat publisher
    # say = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
    # emo = rospy.Publisher('/qt_robot/emotion/show',String, queue_size=10)
    # gesture = rospy.Publisher('comportement/gesture_name',GestureCommand,queue_size=10)
    # rospy.sleep(1)
    # behaviour = RobotBehaviour()
    # name = "bonjour" 
    # behaviour.load_info(name,"Alice")
    # behaviour.realisation()
    
    #print(behaviour.emotion)
    
    

		
    
    
    
