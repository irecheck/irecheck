#!/usr/bin/env python3

import sys
import rospy
import smach
import smach_ros
import pandas as pd
import roslib; roslib.load_manifest('smach_ros')
from std_msgs.msg import String
from numpy.lib.shape_base import split
from datetime import datetime


# define state Greetings
class Greetings(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['default'])

    def execute(self, userdata):
        rospy.loginfo('Executing state GREETINGS')
        print('DO THE WHOLE GREETING PROCEDURE')
        return 'default'

# define state Activity
class Activity(smach.State):
    def __init__(self, activityID):
        smach.State.__init__(self, outcomes=['default','wait'])
        self.newData = False
        self.activityID = activityID
    
    def callback(self, data):
        self.newData = True

    def execute(self, userdata):
        rospy.loginfo('Executing state ACTIVITY')
        rospy.Subscriber('dynamicomsg', String, self.callback)
        if (self.newData == True):
            self.newData = False
            print('PUBLISH APPROPRIATE ROBOT REACTION - ' + self.activityID)
            return 'default'
        else:
            print('WAIT')
            return 'wait'

# define state Goodbye
class Goodbye(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['default'])
        self.pubMsg = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)

    def execute(self, userdata):
        rospy.loginfo('Executing state GOODBYE')
        msg = 'Se la sorte ti e contraria'
        rospy.loginfo(msg)
        self.pubMsg.publish(msg)
        print('DO THE WHOLE GOODBYE PROCEDURE')
        return 'default'


class IrecheckManager():

    def __init__(self):
        self.world = pd.DataFrame()     # dataframe storing all info of relevance for iReCHeCk (sources: Dynamico)

        # initialize ROS node
        rospy.init_node('irecheckmanager', anonymous=True)
        # initialize publishers/subscribers
        # rospy.Subscriber([topic_name],[topic_type],[callback_function_name])
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])

        # Create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['end'])
        # Open the container
        with self.sm:
            # Add states to the container
            smach.StateMachine.add('GREETINGS', Greetings(), 
                               transitions={'default':'ACTIVITY_0'})
            smach.StateMachine.add('ACTIVITY_0', Activity('0'), 
                               transitions={'default':'ACTIVITY_1', 'wait':'ACTIVITY_0'})
            smach.StateMachine.add('ACTIVITY_1', Activity('1'), 
                               transitions={'default':'ACTIVITY_2', 'wait':'ACTIVITY_1'})
            smach.StateMachine.add('ACTIVITY_2', Activity('2'), 
                               transitions={'default':'ASSESSMENT', 'wait':'ACTIVITY_2'})
            smach.StateMachine.add('ASSESSMENT', Activity('as'), 
                               transitions={'default':'GOODBYE', 'wait':'ASSESSMENT'})
            smach.StateMachine.add('GOODBYE', Goodbye(), 
                               transitions={'default':'end'})
        
        # Execute SMACH plan
        outcome = self.sm.execute()

        # keep python from exiting until this node is stopped
        rospy.spin()

    
    # save the dynamico data on the dataframe
    def dynamicoCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')
        # # DEBUG ONLY
        # print(df)
        # append the new record to the dataframe
        self.world = self.world.append(df)
        # fill the empty values with the latest known value for that key
        self.world.fillna( method ='ffill', inplace = True)
        # [DEBUG ONLY]
        print(self.world)
    

    # append a new record to the dataframe
    def addRecord(self,newRecord):
        self.world.loc[len(self.world)] = newRecord
        self.latestRow = self.latestRow + 1
        # [DEBUG ONLY]
        print(self.world)
    

    # save the world dataFrame in a CSV file at the end of the session
    def save2csv(self):
        # backup the dataframe as a CSV file (use current date and time for the file name)
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        filename = '~/Documents/iReCHeCk_logs/' + dt_string + '.csv'
        self.world.to_csv(filename)



#########################################################################
if __name__ == "__main__":
    try:
        myIrecheckManager = IrecheckManager()
    except rospy.ROSInterruptException:
        pass
    finally:
        myIrecheckManager.save2csv()
