#! /usr/bin/env python
import rospy
import tf
from platforms.msg import * 
import numpy as np

## This class contains functions related to tf recognition and publish.

class NuitrackTfTool(object):

	## Initialisation of class
	# @param self The object pointer
	def __init__(self):

		super(NuitrackTfTool, self).__init__()
		## The ids of perced objects
		self.id = []
		## The joints list of skeleton. The length will be 25. Because Nuitrack describe skeleton with 25 joints. Every joint item has information of translation and rotation
		self.joints = []
		## The translations of every joint in space
		self.translation = np.zeros([10,25,3])
		## The rotation of every joint in space
		self.rotation = np.zeros([10,25,9])
		## Transform Broadcaster
		self.br = tf.TransformBroadcaster()


	## Function for load data heard from nuitrack	
	# @param self The object pointer
	# @param data The data heard from nuitrack
	def load_info(self,data):
		# load data of every id 
		for n in range(0,len(data.skeletons)):
			# verifie if this id was detected before
			if data.skeletons[n].id in self.id:
				# if id was detected before, we copy the joint's previous translation and rotation to the translation list and rotation list.
				# Then Overwrite the original data of joints with the new state 
				i = self.id.index(data.skeletons[n].id)
				for j in range(0,25):
					self.translation[i,j,:] = (-np.array(self.joints[i][j].real)/1000.0).tolist()
					self.rotation[i,j,:] = self.joints[i][j].orientation
				self.joints[i] = data.skeletons[n].joints
			else:
				# if not, we will add now id and save data in the joints list,translation list and rotation list
				self.id.append(data.skeletons[n].id)
				i = len(self.id)-1
				self.joints.append(data.skeletons[n].joints)
				for j in range(0,25):
					self.translation[i,j,:] = (-np.array(self.joints[i][j].real)/1000.0).tolist()
					self.rotation[i,j,:] = self.joints[i][j].orientation
		self.do()

	## Function for subscribe nuitrack message
	# @param self The object pointer
	def msg_listener(self):
		""" subscibe nuitrack msg"""
		rospy.init_node("tf_skeletons",anonymous=True)
		rospy.Subscriber('/qt_nuitrack_app/skeletons',Skeletons,self.load_info)
		rospy.spin()

	## Function to send all ids' TFs
	# @param self The object pointer	
	def do(self):
		for i in self.id:
			self.handle_tf(self.id.index(i))


	## Function send Transform information of every point of skeletons
	# @param i The id of detected person
	def handle_tf(self,i):
		# name every joint
		joint_name = ["Head","Neck","Torso","Waist","Left_Collar","Left_Shoulder","Left_Elbow","Left_Wrist","Left_Hand","Right_Collar","Right_Shoulder","Right_Elbow","Right_Wrist","Right_Hand",
					"Left_Hip","Left_Knee","Left_Ankle","Right_Hip","Right_Knee","Right_Ankle"]
		# there a 3 joints don't have data, so we use just 23 joints here.
		joints_number = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,17,18,19,21,22,23]

		# calculate the rotation in Euler angles.
		rot_euler = np.zeros([20,3])
		for (j,n) in zip(joints_number,range(20)): 
			r = self.rotation[i,j,:]
			m = np.mat([[r[0],r[1],r[2]],[r[3],r[4],r[5]],[r[6],r[7],r[8]]])
			rot = tf.transformations.euler_from_matrix(m,"rxyz")
			rot_euler[n,:] = rot
		
		# send transform message
		for (k,j) in zip(joints_number, range(len(joint_name))):
			self.br.sendTransform( self.translation[i,k,:],tf.transformations.quaternion_from_euler(rot_euler[j,0],rot_euler[j,1],rot_euler[j,2]), rospy.Time.now(),joint_name[j]+"_"+str(i),"/nuitrack_frame")


if __name__ == '__main__':
	TF=NuitrackTfTool()
	TF.msg_listener()
