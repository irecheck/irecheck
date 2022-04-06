#!/usr/bin/env python3

# from numpy import arctan2
# from irecheck.scripts.irecheckManager import Assessment
import rospy
import pandas as pd
from std_msgs.msg import String
import threading
import smach 
# import the time module
import time
  

time_out = False


# define state Assessment
class PositiveStreak(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['loss', 'end'],
                             input_keys=['continueKey','timerKey','pubBehMsg','pubMsg'],
                             output_keys=['continueKey','timerKey','pubBehMsg','pubMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state POSITIVE STREAK')
        # stay here until the condition for transitioning is met
        while(userdata.continueKey != True):
            pass 

        # transition to the next state (react the the event and say a proactive sentence)

        if (userdata.timerKey is True):
            userdata.timerKey = False
            userdata.continueKey = False 
            #say good bye
            return 'end'

        if userdata.performance > 1:
            userdata.continueKey = False 
            # insert code to stay here
            print("Good score")
        
        
        if userdata.performance < 1:
            return 'loss'
       
       
        #return 'proceed'

# define state Activity
class NegativeStreak(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['win'],
                             input_keys=['continueKey','getBackKey','pubBehMsg','pubMsg'],
                             output_keys=['continueKey','getBackKey','pubBehMsg','pubMsg'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ACTIVITY')
        # stay here until the condition for transitioning is met
        while((userdata.continueKey == False) & (userdata.getBackKey == False)):
            pass
        # transition to the next state (react the the event and say a proactive sentence)
        # case 1: move on to GOODBYE
        if (userdata.continueKey == True):
            userdata.continueKey = False 
            return 'proceed'
        # case 2: get back to ASSESSMENT
        else:
            userdata.getBackKey = False 
            return 'getBack'

# define state Goodbye
class Goodbye(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['pubBehMsg','pubMsg'],
                             output_keys=['pubBehMsg','pubMsg'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state GOODBYE')
        # wait some time
        rospy.sleep(5)
        # transition to the next state (end)
        msg = 'au_revoir'
        rospy.loginfo(msg)
        userdata.pubBehMsg.publish(msg)   
        return 'proceed'










class DecisionMaker():
    def __init__(self):
        # initialize ROS node
        rospy.init_node('decisionmaker', anonymous=True)
        # initialize publishers/subscribers
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        self.pubFSMMsg = rospy.Publisher('autodecisions', String, queue_size=10)
        self.pubBehMsg = rospy.Publisher('/irecheck/button_name', String, queue_size=1)
        self.pubSayMsg = rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)
        self.world = pd.DataFrame()
        self.round_counter = 0
        
        counter = threading.Thread(target=self.countdown, args=(1,))
        
        counter.start()

        rospy.loginfo("Running and waiting dynamico messages!")
        # keep python from exiting until this node is stopped
        rospy.spin()
     
    # callback on dynamicomsg
    def dynamicoCallback(self, data):
        
        # log the reception of the message
        # rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')
        self.world=self.world.append(df)
        # DEBUG ONLY
        # print(df)

        if time_out:
            print("BOOM")
            msg = 'moveOn'
            rospy.loginfo(msg)
            self.pubFSMMsg.publish(msg)
            exit()
            return
        else:
            print("There is still Time")


        if (len(self.world.index)) == 1:

            print("First entrance. Suggesting based on assessment")
            self.choose_based_on_assessment(df)
        
        elif(len(self.world.index)) > 3:
            self.analyze_streak(3)


        else:
            if (df.at[0, 'score'] > 50 ):
                msg = 'bravo'
                rospy.loginfo(msg)
                self.pubBehMsg.publish(msg)
                msg = 'goToGoodbye'
                rospy.loginfo(msg)
                self.pubFSMMsg.publish(msg)
            else:
                msg = 'courage'
                rospy.loginfo(msg)
                self.pubBehMsg.publish(msg)




        userInput = ''
        
        while 1:
            userInput = input("Type the message: ")

            if userInput == 'assess':
                msg = 'goToAssessment'
                rospy.loginfo(msg)
                self.pubFSMMsg.publish(msg)
                break

            elif userInput == 'act':
                msg = 'goToActivity'
                rospy.loginfo(msg)
                self.pubFSMMsg.publish(msg)
                # self.pubSayMsg.publish(msg)
                break 
            
            elif userInput == 'bye':
                msg = 'moveOn'
                rospy.loginfo(msg)
                self.pubFSMMsg.publish(msg)
                break
            
            else:
                msg = 'Unkown message. Try again!'
                rospy.loginfo(msg)
                
        # print("World-------------:>", self.world)        
        return


    def choose_based_on_assessment(self,df):
        # implement a simple logic to determine what to suggest next
        # if ASSESSMENT --> suggest the activity associated with the lowest score, move to ACTIVITY state
        # if (df.at[0, 'type'] == 'assessment'):
        if (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'pressureScore']):
            msg = 'Jouons au jeu submarine!'
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)
        elif (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'staticScore']):
            msg = 'Jouons au jeu chemist!'
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)
        elif (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'kinematicScore']):
            msg = 'Jouons au jeu pursuit!'
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)
        elif (min([df.at[0, 'pressureScore'],df.at[0, 'staticScore'],df.at[0, 'kinematicScore'],df.at[0, 'tiltScore']]) == df.at[0, 'tiltScore']):
            msg = 'Jouons au jeu copter!'
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)
        else:
            msg = 'Jouons au jeu apprentice!'
            rospy.loginfo(msg)
            self.pubSayMsg.publish(msg)
        
        # msg = 'moveOn'
        # rospy.loginfo(msg)
        # self.pubFSMMsg.publish(msg)  
        
        # if ACTIVITY
        #   if the score in the current game is above 50 --> congratulations, move to GOODBYE state
        #   else --> encouragement and try again
        # else:
        #     if (df.at[0, 'score'] > 50 ):
        #         msg = 'bravo'
        #         rospy.loginfo(msg)
        #         self.pubBehMsg.publish(msg)
        #         msg = 'goToGoodbye'
        #         rospy.loginfo(msg)
        #         self.pubFSMMsg.publish(msg)
        #     else:
        #         msg = 'courage'
        #         rospy.loginfo(msg)
        #         self.pubBehMsg.publish(msg)


    def analyze_streak(self, number):

        last_plays = self.world.iloc[-number]
        print("last ------ ", last_plays)



    # define the countdown func.
    # def countdown(t):
    def countdown(self,minutes):

        t = int(minutes * 60) # makes time in seconds
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

        print('Time is up!!')
        global time_out
        time_out = True

        # # input time in seconds
        # t = input("Enter the time in seconds: ")

        # # function call
        # countdown(int(t))



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
    
    # countdown(30)
    
    try:
        myDecisionMaker = DecisionMaker()
    except rospy.ROSInterruptException:
        pass
