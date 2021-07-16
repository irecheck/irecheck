#!/usr/bin/env python3

import roslib; roslib.load_manifest('smach')
import rospy
import smach
import smach_ros
from std_msgs.msg import String


# define state Sleeping
class Sleeping(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey'],
                             output_keys=['continueKey'])

    def execute(self, userdata):
        rospy.loginfo('Executing state SLEEPING')
        while(userdata.continueKey != True):
            pass
        if (userdata.continueKey == True): 
            userdata.continueKey = False    
            return 'proceed'

# define state Working
class Working(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey'],
                             output_keys=['continueKey'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state WORKING')
        while(userdata.continueKey != True):
            pass
        if (userdata.continueKey == True): 
            userdata.continueKey = False    
            return 'proceed'
        

class TestFSM():
    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.sm.userdata.continueKey = True

    def __init__(self):
        rospy.init_node('smach_fsm')
        rospy.loginfo('2-states FSM that uses ROS topic input to change state')
        rospy.Subscriber('dynamicomsg', String, self.callback)

        # Create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['end'])
        self.sm.userdata.continueKey = False

        # Open the container
        with self.sm:
            # Add states to the container
            smach.StateMachine.add('SLEEPING', Sleeping(), 
                                transitions={'proceed':'WORKING'},
                                remapping={'continueKey':'continueKey', 
                                            'continueKey':'continueKey'})
            smach.StateMachine.add('WORKING', Working(), 
                                transitions={'proceed':'end'},
                                remapping={'continueKey':'continueKey', 
                                            'continueKey':'continueKey'})

        # Execute SMACH plan
        outcome = self.sm.execute()


if __name__ == '__main__':
    try:
        myTestFSM = TestFSM()
    except rospy.ROSInterruptException:
        pass