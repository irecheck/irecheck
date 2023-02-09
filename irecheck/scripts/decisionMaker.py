#!/usr/bin/env python3

# from irecheck.scripts.irecheckManager import Assessment
import rospy
import pandas as pd
from std_msgs.msg import String
import threading
import smach
import time
import sys
  
MINUTES_PER_SESSION = 0.2 #5

SCORE_TO_ACTIVITY_MAP = {
    'pressureScore': 'Submarine',
    'staticScore': 'Chemist',
    'kinematicScore': 'Pursuit',
    'tiltScore': 'Copter'
}

class DummyActivitySuggester:
    """
    A dummy activity recommender based on the lasted evaluation profile 
    """
    def __init__(self) -> None:
        self.evaluation_profile = None
        self.sortedActivitySuggestions = []
        self.currentActivityId = 0

    def get_harder_activity(self):
        self.currentActivityId = (self.currentActivityId - 1) % len(self.sortedActivitySuggestions)
        return self.sortedActivitySuggestions[self.currentActivityId]
    def get_easier_activity(self):
        self.currentActivityId = (self.currentActivityId + 1) % len(self.sortedActivitySuggestions)
        return self.sortedActivitySuggestions[self.currentActivityId]
    
    def update_evaluation_profile(self,evaluation_profile):
        self.currentActivityId = 0
        self.evaluation_profile = evaluation_profile.copy()
        self.sortedActivitySuggestions = [SCORE_TO_ACTIVITY_MAP.get(ele[0]) for ele in self.evaluation_profile]

    
# define state Assessment
class PositiveStreak(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['loss', 'end', 'stay', 'typeChangeAndWin'],
                             input_keys=['continueKey','timerKey', 'performance', 'pubBehMsg','pubMsg', 'pubSayMsg', 'positiveStreakCounter','activitySuggester', 'dynamicoGameType'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg', 'pubSayMsg', 'positiveStreakCounter','activitySuggester'])
        self.currentGameType = ''

    def execute(self, userdata):
        rospy.loginfo('Executing state POSITIVESTREAK')

        self.currentGameType = userdata.dynamicoGameType
        msg = 'moveOn'
        userdata.pubMsg.publish(msg)
        if userdata.positiveStreakCounter >= 1:
            msg = 'pos_streak'
            userdata.pubBehMsg.publish(msg)
            rospy.sleep(2)
            msg = "Let's try a different activity. Let's play {}".format(userdata.activitySuggester.get_harder_activity())
            rospy.loginfo(msg)
            userdata.pubSayMsg.publish(msg)
        else:
            # msg = "Try the next level of the activity"
            # rospy.loginfo(msg)
            # userdata.pubSayMsg.publish(msg)
            # rospy.sleep(2)
            msg = 'go_next_level'
            userdata.pubBehMsg.publish(msg)
            rospy.sleep(2)
            msg = "Play {}".format(userdata.dynamicoGameType)
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
            if (self.currentGameType != userdata.dynamicoGameType):
                # if tried a new type of the game and succeed again, go to single win state
                userdata.positiveStreakCounter = 0
                return 'typeChangeAndWin' 
            else:
                userdata.positiveStreakCounter +=1
                return 'stay'
        
        # Move to single loss state
        if userdata.performance < 1:
            userdata.positiveStreakCounter =0
            return 'loss'

        # default return
        return 'stay'



# define state Win
class Win(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['loss', 'end', 'positiveStreak'],
                             input_keys=['continueKey','timerKey', 'performance', 'pubBehMsg','pubMsg', 'pubSayMsg', 'dynamicoGameType'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg','pubSayMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state SINGLE WIN')

        msg = 'moveOn'
        userdata.pubMsg.publish(msg)


        msg = 'go_next_level'
        userdata.pubBehMsg.publish(msg)
        rospy.sleep(2)
        
        msg = "Play {}".format(userdata.dynamicoGameType)
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
            return 'positiveStreak'
        
        # Move to single loss state
        if userdata.performance < 1:
            return 'loss'

        return 'loss'


# define state Loss
class Loss(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['win', 'end', 'negativeStreak'],
                             input_keys=['continueKey','timerKey','performance', 'pubBehMsg','pubMsg', 'pubSayMsg', 'dynamicoGameType'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg', 'pubSayMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state SINGLE LOSS')
        # stay here until the condition for transitioning is met

        msg = 'moveOn'
        userdata.pubMsg.publish(msg)

        msg = 'keep_the_game'
        userdata.pubBehMsg.publish(msg)
        rospy.sleep(2)

        msg = "Play {}".format(userdata.dynamicoGameType)
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
                             input_keys=['continueKey','timerKey','performance','pubBehMsg','pubMsg', 'pubSayMsg','negativeStreakCounter','activitySuggester', 'dynamicoGameType'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg', 'pubSayMsg', 'negativeStreakCounter','activitySuggester'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state NEGATIVESTREAK')

        msg = 'moveOn'
        userdata.pubMsg.publish(msg)
        if userdata.negativeStreakCounter >= 1:
            msg = 'neg_streak'
            userdata.pubBehMsg.publish(msg)
            rospy.sleep(2)
            msg = "Let's move to a different game. Please play {}".format(userdata.activitySuggester.get_easier_activity())
            rospy.loginfo(msg)
            userdata.pubSayMsg.publish(msg)
        else:
            # msg = "Let's try the same activity again."
            # rospy.loginfo(msg)
            # userdata.pubSayMsg.publish(msg)
            # rospy.sleep(2)
            msg = 'keep_the_game'
            userdata.pubBehMsg.publish(msg)
            rospy.sleep(2)
            msg = "Play {}".format(userdata.dynamicoGameType)
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
            userdata.negativeStreakCounter +=1
            ret =  'stay'
        
        # Move to single win state
        if userdata.performance > 1:
            userdata.negativeStreakCounter =0
            msg = "Lets try to keep the good performance"
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
        rospy.Subscriber('managercommands', String, self.managerCommandsCallback)
        self.world = pd.DataFrame()
        self.round_counter = 0

        # create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['END'])
        # create and initialize the variables to be passed to states
        self.sm.userdata.dynamicoKey = False
        self.sm.userdata.timerKey = False
        self.sm.userdata.dynamicoGameType = '' # submarine, copter, etc.
        self.sm.userdata.performance = 0 # TODO: boolean or not
        self.sm.userdata.positiveStreakCounter = 0
        self.sm.userdata.negativeStreakCounter = 0
        self.sm.userdata.activityOnFocus = ''
        self.sm.userdata.activitySuggester = DummyActivitySuggester()
        self.sm.userdata.pubFSMMsg = self.pubFSMMsg
        self.sm.userdata.pubSayMsg = self.pubSayMsg
        self.sm.userdata.pubBehMsg = self.pubBehMsg
        self.sm.userdata.timer = None

        if len(sys.argv) > 1:
            subject_id = str(sys.argv[1]) # e.g. ID01
        else:
            subject_id = "ID9999999999"
        rospy.loginfo("Starting decisionMaker for subject: {}".format(subject_id))
        
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
                                            'dynamicoGameType': 'dynamicoGameType', 
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
                                            'dynamicoGameType': 'dynamicoGameType', 
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg'})
            
            smach.StateMachine.add('POSITIVESTREAK', PositiveStreak(), 
                                transitions={'loss': 'LOSS',
                                'stay': 'POSITIVESTREAK',
                                'end': 'END',
                                'typeChangeAndWin': 'WIN'},
                                remapping={'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'performance': 'performance',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg', 
                                            'pubSayMsg': 'pubSayMsg',
                                            'positiveStreakCounter': 'positiveStreakCounter',
                                            'activitySuggester': 'activitySuggester', 
                                            'dynamicoGameType': 'dynamicoGameType',
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg',
                                            'positiveStreakCounter': 'positiveStreakCounter',
                                            'activitySuggester': 'activitySuggester'})
            
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
                                            'negativeStreakCounter': 'negativeStreakCounter',
                                            'activitySuggester': 'activitySuggester',
                                            'dynamicoGameType': 'dynamicoGameType',
                                            'continueKey':'dynamicoKey',
                                            'timerKey': 'timerKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubMsg':'pubFSMMsg',
                                            'pubSayMsg': 'pubSayMsg',
                                            'negativeStreakCounter': 'negativeStreakCounter',
                                            'activitySuggester': 'activitySuggester'})

    def run_new_round(self):
        rospy.loginfo("Start a new round of decision maker")
        self.sm.userdata.dynamicoKey = False
        self.sm.userdata.timerKey = False
        self.sm.userdata.performance = 0 # TODO: boolean or not
        self.sm.userdata.positiveStreakCounter = 0
        self.sm.userdata.negativeStreakCounter = 0
        self.sm.userdata.dynamicoGameType = ''
        self.sm.set_initial_state(['IDLE'])

        if self.sm.userdata.activityOnFocus != '':
            # suggest the first activity in the new round
            msg = "Your handwriting is good. Let's play the game: {}".format(self.sm.userdata.activityOnFocus)
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)
            rospy.sleep(5)
            msg = "Please go to the activity and select the game: {}".format(self.sm.userdata.activityOnFocus)
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)

        # execute SMACH plan
        outcome = self.sm.execute()
        rospy.loginfo("OUTCOME: " + outcome)
        rospy.loginfo('Executing state END')
        self.world = pd.DataFrame() # reset world
        rospy.loginfo("Reset dataframe")
        

    def fakeDynamicoCallback(self, data):
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        self.sm.userdata.dynamicoKey = True
        if data.data == 'win':
            self.sm.userdata.performance = 2
        else:
            self.sm.userdata.performance = 0
    
     # callback on dynamicomsg
    def managerCommandsCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        if data.data == 'start_new_round':
            # start timer
            timer = threading.Thread(target=self.countdown, args=(MINUTES_PER_SESSION,))
            timer.start()
            self.run_new_round()

        

     
    # callback on dynamicomsg
    def dynamicoCallback(self, data):        
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')
        self.world=self.world.append(df)
        dynamicoType = df.at[0, 'type']
        
        if 'game' in df.columns:
            dynamicoGameType = df.at[0, 'game']
        else:
            dynamicoGameType = None

        if (len(self.world.index)) == 1 and dynamicoType == 'assessment':
            # only run this block in the new round

            rospy.loginfo("Update evaluation profile and suggest based on assessment")
            self.choose_based_on_assessment(df)            
            self.sm.userdata.dynamicoKey = False # don't execute the state transition for the first assessment

            # inform the irecheck manager to start the activity
            msg = "goToActivity"
            self.pubFSMMsg.publish(msg)

        elif dynamicoType == 'activity':
            if (df.at[0, 'score'] > 30 ):
                msg = 'bravo'
                # rospy.loginfo(msg)
                self.pubBehMsg.publish(msg)
                rospy.sleep(5)
                self.sm.userdata.performance = 2
            else:
                msg = 'courage'
                # rospy.loginfo(msg)
                self.pubBehMsg.publish(msg)
                rospy.sleep(5)
                self.sm.userdata.performance = 0
            self.sm.userdata.dynamicoKey = True
            self.sm.userdata.dynamicoGameType = dynamicoGameType

            # FOR INFINITE TIME, CHANGE HERE
            if(self.sm.userdata.timerKey):
                msg = 'goToAssessment'
                self.pubFSMMsg.publish(msg)

        else:
            self.sm.userdata.dynamicoKey = False





    def choose_based_on_assessment(self,df):
        # implement a simple logic to determine what to suggest next
        # if ASSESSMENT --> suggest the activity associated with the lowest score, move to ACTIVITY state

        eval_profile = df.loc[0, ['pressureScore', 'staticScore', 'kinematicScore', 'tiltScore']].copy()
        eval_profile = list(eval_profile.to_dict().items())
        eval_profile.sort(key = lambda x: x[1])
        rospy.loginfo("Eval profile: {}".format(eval_profile))
        self.sm.userdata.activitySuggester.update_evaluation_profile(eval_profile)
        rospy.loginfo("Sorted Activity Suggestions: {}".format(self.sm.userdata.activitySuggester.sortedActivitySuggestions))
        self.sm.userdata.activityOnFocus = self.sm.userdata.activitySuggester.sortedActivitySuggestions[0]


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



#########################################################################
if __name__ == "__main__":
    # To test this module, run:
    # rostopic pub -1 /managercommands std_msgs/String start_new_round

    try:
        myDecisionMaker = DecisionMaker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
