#!/usr/bin/env python3

# from numpy import arctan2
# from irecheck.scripts.irecheckManager import Assessment
import rospy
import pandas as pd
from rospy.topics import Publisher
from std_msgs.msg import String
import threading
import smach 
# import the time module
import time
  
MINUTES_PER_SESSION = 5

# define state Assessment
class PositiveStreak(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['loss', 'end', 'stay'],
                             input_keys=['continueKey','timerKey', 'performance', 'pubBehMsg','pubMsg', 'pubSayMsg'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg', 'pubSayMsg'])
        self.positiveStreakCounter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state POSITIVESTREAK')

        msg = 'moveOn'
        userdata.pubMsg.publish(msg)
        if self.positiveStreakCounter >= 1:
            msg = "Wow, you are really good at it, try a harder game"
            rospy.loginfo(msg)
            userdata.pubSayMsg.publish(msg)
            # print("Good score! Let's play the next available level", userdata.activityOnFocus)
        else:
            msg = "Well done, try the next game"
            rospy.loginfo(msg)
            userdata.pubSayMsg.publish(msg)
        rospy.sleep(2)

        # wait untill the previous activity is finished
        while(userdata.continueKey != True):
            pass 
        userdata.continueKey = False 

        # transition to final state due to time up
        if (userdata.timerKey is True):
            userdata.timerKey = False
            #say good bye
            msg = 'goToEndAssessment'
            userdata.pubMsg.publish(msg)
            return 'end'

        # Move to positive Streak state
        if userdata.performance > 1:
            self.positiveStreakCounter +=1
            return 'stay'
        
        # Move to single loss state
        if userdata.performance < 1:
            self.positiveStreakCounter =0
            return 'loss'

        # default return
        return 'stay'



# define state Win
class Win(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['loss', 'end', 'positiveStreak'],
                             input_keys=['continueKey','timerKey', 'performance', 'pubBehMsg','pubMsg', 'pubSayMsg'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg','pubSayMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state SINGLE WIN')

        msg = 'moveOn'
        userdata.pubMsg.publish(msg)
        
        msg = "Select the next level of the game"
        rospy.loginfo(msg)
        userdata.pubSayMsg.publish(msg)
        rospy.sleep(2)

        # wait until the previous activity is finished
        while(userdata.continueKey != True):
            pass
        userdata.continueKey = False 

        # transition to final state due to time up
        if (userdata.timerKey is True):
            userdata.timerKey = False
            #say good bye
            msg = 'goToEndAssessment'
            userdata.pubMsg.publish(msg)
            return 'end'

        # Move to positive Streak state
        if userdata.performance > 1:
            ret = 'positiveStreak'
        
        # Move to single loss state
        if userdata.performance < 1:
            ret = 'loss'

        return ret


# define state Loss
class Loss(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['win', 'end', 'negativeStreak'],
                             input_keys=['continueKey','timerKey','performance', 'pubBehMsg','pubMsg', 'pubSayMsg'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg', 'pubSayMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state SINGLE LOSS')
        # stay here until the condition for transitioning is met

        msg = 'moveOn'
        userdata.pubMsg.publish(msg)
        msg = "The score is a bit lower. But don't worry, it's just a single fail, let's try the same game again"
        rospy.loginfo(msg)
        userdata.pubSayMsg.publish(msg)
        rospy.sleep(2)
        
        
        # wait until the previous activity is finished
        while(userdata.continueKey != True):
            pass 
        userdata.continueKey = False

        # transition to final state due to time up
        if (userdata.timerKey is True):
            userdata.timerKey = False
            #say good bye
            msg = 'goToEndAssessment'
            userdata.pubMsg.publish(msg)
            return 'end'

        # Move to negative Streak state
        if userdata.performance < 1:
            # insert code to stay here
            ret = 'negativeStreak'
        
        # Move to single win state
        if userdata.performance > 1:
            ret = 'win'

        return ret



# define state Negative Streak
class NegativeStreak(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['win', 'end', 'stay'],
                             input_keys=['continueKey','timerKey','performance','pubBehMsg','pubMsg', 'pubSayMsg'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg', 'pubSayMsg'])
        self.negativeStreakCounter = 0
    def execute(self, userdata):
        rospy.loginfo('Executing state NEGATIVESTREAK')

        msg = 'moveOn'
        userdata.pubMsg.publish(msg)
        if self.negativeStreakCounter >= 1:
            msg = "It seems that you are tired of it. Try a easier activity"
            rospy.loginfo(msg)
            userdata.pubSayMsg.publish(msg)
            # print("Bad score again! Let's play the previous level of ", userdata.activityOnFocus)
        else:
            msg = "Cheer up. Let's try it again."
            rospy.loginfo(msg)
            userdata.pubSayMsg.publish(msg)
        rospy.sleep(2)

        # wait untill the previous activity is finished
        while(userdata.continueKey != True):
            pass
        userdata.continueKey = False 

        # transition to final state due to time up
        if (userdata.timerKey is True):
            userdata.timerKey = False
            #say good bye
            msg = 'goToEndAssessment'
            userdata.pubMsg.publish(msg)
            return 'end'

        # keeps in Negative Streak state
        if userdata.performance < 1:
            self.negativeStreakCounter +=1
            ret =  'stay'
        
        # Move to single win state
        if userdata.performance > 1:
            self.positiveStreakCounter =0
            msg = "Well done! Lets try to keep the good performance"
            rospy.loginfo(msg)
            userdata.pubSayMsg.publish(msg)
            rospy.sleep(2)
            ret =  'win'

        return ret

# define state Win
class Idle(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['win', 'loss', 'end'],
                             input_keys=['continueKey','timerKey','performance', 'pubBehMsg','pubMsg', 'pubSayMsg'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg', 'pubSayMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state Idle')
        
        # wait untill the first activity is finished
        while(userdata.continueKey != True):
            pass 
        userdata.continueKey = False 

        # transition to final state due to time up
        if (userdata.timerKey is True):
            userdata.timerKey = False
            #say good bye
            return 'end'

        # Move to positive Streak state
        if userdata.performance > 1:
            ret = 'win'
        
        # Move to single loss state
        if userdata.performance < 1:
            ret = 'loss'

        return ret







class DecisionMaker():
    def __init__(self):
        # initialize ROS node
        rospy.init_node('decisionmaker', anonymous=True)
        # initialize publishers/subscribers
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        # rospy.Subscriber('dynamicomsg', String, self.fakeDynamicoCallback)
        self.pubFSMMsg = rospy.Publisher('autodecisions', String, queue_size=10)
        self.pubBehMsg = rospy.Publisher('/irecheck/button_name', String, queue_size=1)
        self.pubSayMsg = rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)
        self.world = pd.DataFrame()
        self.round_counter = 0

        # create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['END'])
        # create and initialize the variables to be passed to states
        self.sm.userdata.dynamicoKey = False
        self.sm.userdata.timerKey = False
        self.sm.userdata.performance = 0 # TODO: boolean or not
        self.sm.userdata.positiveStreakCounter = 0
        self.sm.userdata.negativeStreakCounter = 0
        self.sm.userdata.activityOnFocus = "Select an activity"
        self.sm.userdata.pubFSMMsg = self.pubFSMMsg
        self.sm.userdata.pubSayMsg = self.pubSayMsg
        self.sm.userdata.pubBehMsg = self.pubBehMsg
        
        with self.sm:
            # Add states to the container

            smach.StateMachine.add('IDLE', Idle(), 
                                transitions={'win':'WIN',
                                             'loss': 'LOSS',
                                             'end': 'END'},
                                remapping={'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'performance': 'performance',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg', 
                                            'pubSayMsg': 'pubSayMsg',
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg'})
            
            smach.StateMachine.add('WIN', Win(), 
                                transitions={'positiveStreak':'POSITIVESTREAK',
                                             'loss': 'LOSS',
                                             'end': 'END'},
                                remapping={'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'performance': 'performance',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg', 
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg'})
            
            
            smach.StateMachine.add('LOSS', Loss(), 
                                transitions={'win':'WIN',
                                             'negativeStreak': 'NEGATIVESTREAK',
                                             'end': 'END'},
                                remapping={'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'performance': 'performance',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg', 
                                            'pubSayMsg': 'pubSayMsg', 
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg'})
            
            smach.StateMachine.add('POSITIVESTREAK', PositiveStreak(), 
                                transitions={'loss': 'LOSS',
                                'stay': 'POSITIVESTREAK',
                                'end': 'END'},
                                remapping={'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'performance': 'performance',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg', 
                                            'pubSayMsg': 'pubSayMsg', 
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg'})
            
            smach.StateMachine.add('NEGATIVESTREAK', NegativeStreak(), 
                                transitions={'win':'WIN',
                                'stay': 'NEGATIVESTREAK',
                                'end': 'END'},
                                remapping={'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'performance': 'performance',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg', 
                                            'pubSayMsg': 'pubSayMsg', 
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg'})
        self.sm.set_initial_state(['IDLE'])

        # start counter
        counter = threading.Thread(target=self.countdown, args=(MINUTES_PER_SESSION,))
        counter.start()
        # execute SMACH plan
        outcome = self.sm.execute()
        
        rospy.loginfo("OUTCOME: " + outcome)

        # keep python from exiting until this node is stopped
        rospy.spin()

    def fakeDynamicoCallback(self, data):
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        self.sm.userdata.dynamicoKey = True
        if data.data == 'win':
            self.sm.userdata.performance = 2
        else:
            self.sm.userdata.performance = 0

        

     
    # callback on dynamicomsg
    def dynamicoCallback(self, data):
        # TODO: what to suggest
        
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')
        self.world=self.world.append(df)

        if (len(self.world.index)) == 1:

            rospy.loginfo("First entrance. Suggesting based on assessment")
            self.choose_based_on_assessment(df)
            msg = "Your handwriting is good. Let's play the game: {}".format(self.sm.userdata.activityOnFocus)
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)
            rospy.sleep(5)
            msg = "Please go to the activity and select the game: {}".format(self.sm.userdata.activityOnFocus)
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)

            # print("Let's focus on game: ", self.sm.userdata.activityOnFocus)
            self.sm.userdata.dynamicoKey = False # don't execute the state transition for the first assessment

            # inform the irecheck manager to start the activity
            msg = "goToActivity"
            self.pubFSMMsg.publish(msg)

        else:
            if (df.at[0, 'score'] > 85 ):
                msg = 'bravo'
                # rospy.loginfo(msg)
                self.pubBehMsg.publish(msg)
                self.sm.userdata.performance = 2
            else:
                msg = 'courage'
                # rospy.loginfo(msg)
                self.pubBehMsg.publish(msg)
                self.sm.userdata.performance = 0
            self.sm.userdata.dynamicoKey = True

    def choose_based_on_assessment(self,df):
        # implement a simple logic to determine what to suggest next
        # if ASSESSMENT --> suggest the activity associated with the lowest score, move to ACTIVITY state
        # if (df.at[0, 'type'] == 'assessment'):
        if (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'pressureScore']):
            self.sm.userdata.activityOnFocus = 'Submarine'
        elif (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'staticScore']):
            self.sm.userdata.activityOnFocus = 'Chemist'
        elif (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'kinematicScore']):
            self.sm.userdata.activityOnFocus = 'Pursuit'
        elif (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'tiltScore']):
            self.sm.userdata.activityOnFocus = 'Copter'
        else:
            self.sm.userdata.activityOnFocus = 'Apprentice'
        


    def analyze_streak(self, number):

        last_plays = self.world.iloc[-number]
        print("last ------ ", last_plays)



    # define the countdown func.
    def countdown(self,minutes):

        t = int(minutes * 60) # makes time in seconds
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

        print('Time is up!!')
        self.sm.userdata.timerKey = True



'''
        - Assessment
        - Take the worst skill to suggest
        - IF score < 50:
            - give another change and acummulate 1 error
        - IF score < 50 again:
            - Take the game with highest score in the game-log (dataframe) 
            OR a game related to the highest skill from the assessment
        - 


'''


#########################################################################
if __name__ == "__main__":
        
    try:
        myDecisionMaker = DecisionMaker()
    except rospy.ROSInterruptException:
        pass
