#!/usr/bin/env python3

import rospy
import smach
import roslib; roslib.load_manifest('smach')
from std_msgs.msg import String


# define state Sleeping
class Sleeping(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey','pubMsg'],
                             output_keys=['continueKey','pubMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state SLEEPING')
        # stay here until the condition for transitioning is met
        while(userdata.continueKey != True):
            pass
        # transition to the next state
        userdata.continueKey = False
        msg = 'bonjour'
        rospy.loginfo(msg)
        userdata.pubMsg.publish(msg)   
        return 'proceed'

# define state Activity
class Activity(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey','pubMsg'],
                             output_keys=['continueKey','pubMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ACTIVITY')
        # stay here until the condition for transitioning is met
        while(userdata.continueKey != True):
            pass
        # transition to the next state
        userdata.continueKey = False
        msg = 'bravo'
        rospy.loginfo(msg)
        userdata.pubMsg.publish(msg)   
        return 'proceed'

# define state Assessment
class Assessment(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey','pubMsg'],
                             output_keys=['continueKey','pubMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ASSESSMENT')
        # stay here until the condition for transitioning is met
        while(userdata.continueKey != True):
            pass
        # transition to the next state
        userdata.continueKey = False
        msg = 'bravo'
        rospy.loginfo(msg)
        userdata.pubMsg.publish(msg)   
        return 'proceed'

# define state Goodbye
class Goodbye(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['pubMsg'],
                             output_keys=['pubMsg'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state GOODBYE')
        # wait some time
        rospy.sleep(5)
        # transition to the next state (end)
        msg = 'au revoir'
        rospy.loginfo(msg)
        userdata.pubMsg.publish(msg)   
        return 'proceed'



class IrecheckManager():
    def __init__(self):
        # initialize ROS node
        rospy.init_node('irecheckmanager', anonymous=True)
        # initialize subscribers
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        rospy.Subscriber('qt_nuitrack_app/faces', Faces, self.nuitrackCallback)
        
        # create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['end'])
        # create and initialize the variables to be passed to states
        self.sm.userdata.dynamicoKey = False
        self.sm.userdata.faceKey = False
        self.sm.userdata.pubMsg = rospy.Publisher('/irecheck/button_name', String, queue_size=1)

        # open the container
        with self.sm:
            # Add states to the container
            smach.StateMachine.add('SLEEPING', Sleeping(), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'faceKey',
                                            'pubMsg':'pubMsg', 
                                            'continueKey':'faceKey',
                                            'pubMsg':'pubMsg'})
            smach.StateMachine.add('ACTIVITY', Activity(), 
                                transitions={'proceed':'ASSESSMENT'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubMsg':'pubMsg', 
                                            'continueKey':'dynamicoKey',
                                            'pubMsg':'pubMsg'})
            smach.StateMachine.add('ASSESSMENT', Assessment(), 
                                transitions={'proceed':'GOODBYE'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubMsg':'pubMsg', 
                                            'continueKey':'dynamicoKey',
                                            'pubMsg':'pubMsg'})
            smach.StateMachine.add('GOODBYE', Goodbye(), 
                                transitions={'proceed':'end'},
                                remapping={'pubMsg':'pubMsg', 
                                            'pubMsg':'pubMsg'})
        
        # execute SMACH plan
        outcome = self.sm.execute()
        rospy.loginfo("OUTCOME: " + outcome)
 
    # callback on dynamicomsg
    def dynamicoCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # notify the FSM of the arrival of new dynamico data
        self.sm.userdata.dynamicoKey = True

    # callback on nuitrack/faces
    def nuitrackCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # notify the FSM of the detection of a face
        self.sm.userdata.faceKey = True



#########################################################################
if __name__ == "__main__":
    try:
        myIrecheckManager = IrecheckManager()
    except rospy.ROSInterruptException:
        pass
