#!/usr/bin/env python3

import roslib; roslib.load_manifest('smach')
import rospy
import smach
import smach_ros

# define state Sleeping
class Sleeping(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed','quit'],
                             input_keys=['continueKey'],
                             output_keys=['continueKey'])

    def execute(self, userdata):
        rospy.loginfo('Executing state SLEEPING')
        while(userdata.continueKey != '0') & (userdata.continueKey != '1'):
            userdata.continueKey = input('Type 1 to wakeUp, 0 to quit: ')
            print('You chose: ' + userdata.continueKey)
        if userdata.continueKey == '1':
            userdata.continueKey = '2'    
            return 'proceed'
        if userdata.continueKey == '0':
            return 'quit'


# define state Working
class Working(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed','quit'],
                             input_keys=['continueKey'],
                             output_keys=['continueKey'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state WORKING')
        while(userdata.continueKey != '0') & (userdata.continueKey != '1'):
            userdata.continueKey = input('Type 1 to goSleep, 0 to quit: ')
            print('You chose: ' + userdata.continueKey)
        if userdata.continueKey == '1':
            userdata.continueKey = '2'    
            return 'proceed'
        if userdata.continueKey == '0':
            return 'quit'
        




def main():
    rospy.init_node('smach_fsm')
    rospy.loginfo('2-states FSM that uses keyboard input to change state')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['end'])
    sm.userdata.continueKey = '2'

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('SLEEPING', Sleeping(), 
                               transitions={'proceed':'WORKING', 
                                            'quit':'end'},
                               remapping={'continueKey':'continueKey', 
                                          'continueKey':'continueKey'})
        smach.StateMachine.add('WORKING', Working(), 
                               transitions={'proceed':'SLEEPING',
                                            'quit':'end'},
                               remapping={'continueKey':'continueKey', 
                                          'continueKey':'continueKey'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':
    main()