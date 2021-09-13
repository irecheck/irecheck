#!/usr/bin/env python3

import rospy
import smach
import pandas as pd
import roslib; roslib.load_manifest('smach')
from std_msgs.msg import String
from qt_nuitrack_app.msg import *
from datetime import datetime

# define state Sleeping
class Sleeping(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey','pubBehMsg','robotSay'],
                             output_keys=['continueKey','pubBehMsg','robotSay'])


    def execute(self, userdata):
        rospy.loginfo('Executing state SLEEPING')
        # stay here until the condition for transitioning is met
        while(userdata.continueKey != True):
            pass
        # transition to the next state (react the the event and say a proactive sentence)
        userdata.continueKey = False
        msg = 'bonjour'
        rospy.loginfo(msg)
        userdata.pubBehMsg.publish(msg) 
        rospy.sleep(5)

        msg = "Please take this seat"
        rospy.loginfo(msg)
        userdata.robotSay.publish(msg)   
        rospy.sleep(5)

        # msg = 'Commençons par dessiner un chat!'
        msg = "Let's start the interaction!"
        rospy.loginfo(msg)
        userdata.robotSay.publish(msg)   
        return 'proceed'

# define state Assessment
class Assessment(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey','pubBehMsg','robotSay'],
                             output_keys=['continueKey','pubBehMsg','robotSay'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ASSESSMENT')

        msg = "It is time to check how your handwriting is going. Please ... "
        userdata.robotSay(msg)
        rospy.loginfo(msg)


        # stay here until the condition for transitioning is met
        while(userdata.continueKey != True):
            pass
        # transition to the next state (react the the event and say a proactive sentence)
        userdata.continueKey = False 
        return 'proceed'


# define state Activity
class Activity(smach.State):
        
    def __init__(self, activity_name):
        self.activity_name = activity_name
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey','pubBehMsg','robotSay'],
                             output_keys=['continueKey','pubBehMsg','robotSay'])
        

    def execute(self, userdata):

        rospy.loginfo('Executing state ACTIVITY')

        msg = "Now, let's play the next available level of the activity: " + self.activity_name
        userdata.robotSay(msg)
        rospy.loginfo(msg)
        
        
        # stay here until the condition for transitioning is met
        while(userdata.continueKey != True):
            pass
        # transition to the next state (react the the event and say a proactive sentence)
        userdata.continueKey = False 

        msg = "Great! I see that you finished this activity. Let's move to the next one." 
        userdata.robotSay(msg)
        rospy.loginfo(msg)
        

        return 'proceed'


# define state Activity
# class Activity(smach.State):
#     def __init__(self):
#         smach.State.__init__(self, 
#                              outcomes=['proceed'],
#                              input_keys=['continueKey','pubBehMsg','robotSay'],
#                              output_keys=['continueKey','pubBehMsg','robotSay'])

#     def execute(self, userdata):
#         rospy.loginfo('Executing state ACTIVITY')
#         # stay here until the condition for transitioning is met
#         while(userdata.continueKey != True):
#             pass
#         # transition to the next state (react the the event and say a proactive sentence)
#         userdata.continueKey = False 
#         return 'proceed'



# define state Goodbye
class Goodbye(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['pubBehMsg','robotSay'],
                             output_keys=['pubBehMsg','robotSay'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state GOODBYE')
        # wait some time
        rospy.sleep(5)
        # transition to the next state (end)
        msg = 'au_revoir'
        rospy.loginfo(msg)
        userdata.pubBehMsg.publish(msg)   
        return 'proceed'



class IrecheckManager():
    def __init__(self):
        self.world = pd.DataFrame()     # dataframe storing all info of relevance for iReCHeCk (sources: Dynamico)

        # initialize ROS node
        rospy.init_node('irecheckmanager', anonymous=True)
        # initialize subscribers
        rospy.Subscriber('/qt_nuitrack_app/faces', Faces, self.nuitrackCallback)
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        rospy.Subscriber('autodecisions', String, self.decisionsCallback)

        # create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['end'])
        # create and initialize the variables to be passed to states
        self.sm.userdata.faceKey = False
        self.sm.userdata.dynamicoKey = False
        self.sm.userdata.decisionsKey = False
        self.sm.userdata.pubBehMsg = rospy.Publisher('/irecheck/button_name', String, queue_size=1)
        self.sm.userdata.robotSay = rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)

        # open the container
        with self.sm:
            # Add states to the container
            smach.StateMachine.add('SLEEPING', Sleeping(), 
                                transitions={'proceed':'ASSESSMENT'},
                                remapping={'continueKey':'faceKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'faceKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
        
            smach.StateMachine.add('ASSESSMENT', Assessment(), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
            
            # pursuit 1
            smach.StateMachine.add('ACTIVITY', Activity('pusruit'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
        
            # pursuit 2
            smach.StateMachine.add('ACTIVITY', Activity('pusruit'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
        
            # pursuit 3
            smach.StateMachine.add('ACTIVITY', Activity('pusruit'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # submarine
            smach.StateMachine.add('ACTIVITY', Activity('submarine'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # copter
            smach.StateMachine.add('ACTIVITY', Activity('copter'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # chemist 1
            smach.StateMachine.add('ACTIVITY', Activity('chemist'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # chemist 2
            smach.StateMachine.add('ACTIVITY', Activity('chemist'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # chemist 3
            smach.StateMachine.add('ACTIVITY', Activity('chemist'), 
                                transitions={'proceed':'GOODBYE'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
        
            smach.StateMachine.add('GOODBYE', Goodbye(), 
                                transitions={'proceed':'end'},
                                remapping={'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay',
                                            'pubBehMsg':'pubBehMsg', 
                                            'robotSay':'robotSay'})
        
        # I am not sure if this works
        # Adding three rounds of activity
        # self.addRound()
        #self.addRound()
        #self.addRound()
        
        #     smach.StateMachine.add('ASSESSMENT', Assessment(), 
        #                         transitions={'proceed':'ACTIVITY'},
        #                         remapping={'continueKey':'decisionsKey',
        #                                     'pubBehMsg':'pubBehMsg',
        #                                     'robotSay':'robotSay', 
        #                                     'continueKey':'decisionsKey',
        #                                     'pubBehMsg':'pubBehMsg',
        #                                     'robotSay':'robotSay'})
        #     smach.StateMachine.add('ACTIVITY', Activity(), 
        #                         transitions={'proceed':'GOODBYE'},
        #                         remapping={'continueKey':'decisionsKey',
        #                                     'pubBehMsg':'pubBehMsg',
        #                                     'robotSay':'robotSay', 
        #                                     'continueKey':'decisionsKey',
        #                                     'pubBehMsg':'pubBehMsg',
        #                                     'robotSay':'robotSay'})
        
        # # open the container
       # with self.sm:
        # execute SMACH plan
        outcome = self.sm.execute()
        rospy.loginfo("OUTCOME: " + outcome)
 
    
    # add one round of activities
    def addRound(self):
            
        with self.sm:

            smach.StateMachine.add('ASSESSMENT', Assessment(), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
            
            # pursuit 1
            smach.StateMachine.add('ACTIVITY', Activity('pusruit'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
        
            # pursuit 2
            smach.StateMachine.add('ACTIVITY', Activity('pusruit'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
        
            # pursuit 3
            smach.StateMachine.add('ACTIVITY', Activity('pusruit'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # submarine
            smach.StateMachine.add('ACTIVITY', Activity('submarine'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # copter
            smach.StateMachine.add('ACTIVITY', Activity('copter'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # chemist 1
            smach.StateMachine.add('ACTIVITY', Activity('chemist'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # chemist 2
            smach.StateMachine.add('ACTIVITY', Activity('chemist'), 
                                transitions={'proceed':'ACTIVITY'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            # chemist 3
            smach.StateMachine.add('ACTIVITY', Activity('chemist'), 
                                transitions={'proceed':'GOODBYE'},
                                remapping={'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'dynamicoKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})


            


    
    
    # callback on dynamicomsg
    def dynamicoCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # notify the FSM of the arrival of new dynamico data
        self.sm.userdata.dynamicoKey = True
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')
        # # DEBUG ONLY
        # print(df)
        # append the new record to the dataframe
        self.world = self.world.append(df)
        # fill the empty values with the latest known value for that key
        self.world.fillna( method ='ffill', inplace = True)
        # # [DEBUG ONLY]
        # print(self.world)

    # callback on nuitrack/faces
    def nuitrackCallback(self, data):
        # log the reception of the message
        #rospy.loginfo(rospy.get_caller_id() + '- received %s', data.faces)
        rospy.loginfo(rospy.get_caller_id() + '- received face')
        # notify the FSM of the detection of a face
        self.sm.userdata.faceKey = True

    # callback on autodecisions
    def decisionsCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # notify the FSM of the arrival of new decisions data
        # for now it makes the FSM proceed to the next state
        self.sm.userdata.decisionsKey = True
    
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
