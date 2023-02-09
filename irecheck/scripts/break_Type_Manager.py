#!/usr/bin/env python3

 
import rospy
import smach
import pandas as pd
import roslib; roslib.load_manifest('smach')
from std_msgs.msg import String
from qt_nuitrack_app.msg import Faces
from datetime import datetime
import sys

NUM_OF_ROUNDS = 2

BREAK_COUNTER = 0
NUMBER_BREAKS = 1

CONDITION_OPTIONS = ['breathe', 'stretch']
EXPERIMENT_CONDITION = CONDITION_OPTIONS[1]

robot_connected = False

CURRENT_ROUND = 0

class global_robotSay():



    if robot_connected:

        def publish(sentence):
            speechSay = rospy.ServiceProxy('/qt_robot/behavior/talkText', speech_say)
            # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
            # rospy.wait_for_service('/qt_robot/speech/say')
            rospy.wait_for_service('/qt_robot/behavior/talkText')
            speechSay(sentence)
    
    else:
        
        def publish(sentence):
            rospy.loginfo(sentence)


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
        rospy.sleep(5)   
        return 'proceed'

# define state Assessment
class Assessment(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed', 'bye'],
                             input_keys=['continueKey','pubBehMsg','robotSay','isEndAssessment','pubCommandMsg'], # TODO: isEndAssessment may be unnecessary
                             output_keys=['continueKey','pubBehMsg','robotSay', 'isEndAssessment', 'pubCommandMsg'])

        self.assessment_counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state ASSESSMENT')
        
        msg = "It is time to check how your handwriting is going. Please perform an evaluation. It could take a while for me to compute it after you finish."
        userdata.robotSay.publish(msg)
        rospy.loginfo(msg)
        rospy.sleep(2)


        while(userdata.continueKey != True):
            pass
        userdata.continueKey = False
        self.assessment_counter = self.assessment_counter + 1
        rospy.loginfo('Finish {} assessment'.format(self.assessment_counter))
        if self.assessment_counter <= NUM_OF_ROUNDS:
            rospy.loginfo('Start the {} round of activities'.format(self.assessment_counter))
            msg = 'start_new_round'
            userdata.pubCommandMsg.publish(msg) 

        # msg = "Great!"
        # userdata.robotSay.publish(msg)
        # rospy.loginfo(msg)

        # if userdata.isEndAssessment and self.assessment_counter > NUM_OF_ROUNDS:
        if self.assessment_counter >= NUM_OF_ROUNDS:
            # if this is the assessment ordered by the decisionMaker, go to the GoodBye state
            return 'bye'
        else:
            userdata.isEndAssessment = False
            return 'proceed'

# define state Activity
class Activity(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed','getBack','stay','break'],
                             input_keys=['continueKey','getBackKey','pubBehMsg','robotSay'],
                             output_keys=['continueKey','getBackKey','pubBehMsg','robotSay'])

    def execute(self, userdata):
        rospy.loginfo('Executing state ACTIVITY')
        # stay here until the condition for transitioning is met
        while((userdata.continueKey is False) and (userdata.getBackKey is False) ):
            pass
        # transition to the next state (react the the event and say a proactive sentence)
       
        # case 1: move on to next activity
        if ((userdata.continueKey is True) and (userdata.getBackKey is False) ):
            userdata.continueKey = False 
            return 'stay'
        # case 2: get back to ASSESSMENT
        elif ((userdata.continueKey is False) and (userdata.getBackKey is True) ):
            
            # if break didnt happen yet, make a break. Otherwise, send to the last evaluation to finish
            #SHOULD RETHINK IT BETTER LATER (consider the round number here)
            # global BREAK_COUNTER
            # global NUMBER_BREAKS
            # print("------------------------  BREAK_COUNTER", int(BREAK_COUNTER))
            # print("NUMBER_BREAKS", NUMBER_BREAKS)
            # if BREAK_COUNTER <= NUMBER_BREAKS:
            #     BREAK_COUNTER += 1
            #     return 'break'
            # else:
            #     return 'getBack'
            return 'getBack'
        # case 3: take to BREAK
        # elif ((userdata.continueKey is False) and (userdata.getBackKey is False) and (userdata.breakKey is True)):
        #     return 'break'
        
        # case 4: go to GOODBYE state (should not be reached by design)
        else:
            return 'proceed'

# define state Goodbye
class Goodbye(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['pubBehMsg','robotSay'],
                             output_keys=['pubBehMsg','robotSay'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state GOODBYE')

        msg = "Okay my little friend. This is the end of the session. It was nice to have fun with you!"
        userdata.robotSay.publish(msg)
        rospy.loginfo(msg)
        rospy.sleep(5)

        # transition to the next state (end)
        msg = 'au_revoir'
        rospy.loginfo(msg)
        userdata.pubBehMsg.publish(msg)
        # wait some time
        rospy.sleep(5)   
        return 'proceed'




# --------------------------------- Breaking Classes



class Break(smach.State):
  
    """All the stretching movements."""
    
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['proceed'],
                            input_keys=['pubBehMsg','robotSay'],
                            output_keys=['pubBehMsg','robotSay'])

    def execute(self, userdata):
  
        if CURRENT_ROUND == NUM_OF_ROUNDS:
            return 'proceed'
  
        rospy.loginfo('Starting break session')

        # building the function name
        function_name = "self." + EXPERIMENT_CONDITION + "(userdata)"

        # return the return of the executed function which should be proceed
        return eval(function_name)


    def breathe(self, userdata):
        
        rospy.loginfo('Executing breathing state')
        msg = 'We are now going to do some deep breathing !'
        userdata.robotSay.publish(msg)
        

        msg = 'Sit straight in your chair.'
        userdata.robotSay.publish(msg)
        
        msg = 'We are going to start. When I say in, inhale through the nose. When I say out, exhale through the mouth'
        userdata.robotSay.publish(msg)
                
        rospy.sleep(1.)
        
        for i in range(2):
            msg = "In"
            userdata.robotSay.publish(msg)
            rospy.sleep(2)
            
            msg = "Out"
            userdata.robotSay.publish(msg)
            rospy.sleep(2)
        
        msg = 'That is it !'
        userdata.robotSay.publish(msg)

        return 'proceed'

    
    def stretch(self, userdata):

        # emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
        # rospy.wait_for_service('/qt_robot/emotion/show')
        # emotionShow('QT/neutral')

        # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        # rospy.wait_for_service('/qt_robot/speech/say')
        # speechSay("I stood still for a very long time, I really need some stretching !")

        # gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        # rospy.wait_for_service('/qt_robot/gesture/play')
        # gesturePlay('stretch', 1)
 
        # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        # rospy.wait_for_service('/qt_robot/speech/say')
        # speechSay("Lets do a stretch session together, it will be fun !")

        # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        # rospy.wait_for_service('/qt_robot/speech/say')
        # speechSay("We start with the head. I will show you how to do each stretch. Your stretch should last at least five seconds and I will count to five when you do it.")
       
        msg = ("We start with the head. I will show you how to do each stretch. Your stretch should last at least five seconds and I will count to five when you do it.")
       
        userdata.robotSay.publish(msg)
       
        # added
        # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        # rospy.wait_for_service('/qt_robot/speech/say')
        # speechSay("You should start stretching when I show you how to do it. But you need to maintain the position for more time than me, until I finish counting.")
        # gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        # rospy.wait_for_service('/qt_robot/gesture/play')
        # gesturePlay('head_left', 1.5)

        # seconds = 0
        # start_time = time.time()
        numbers = ['one', 'two', 'three', 'four', 'five']
        

        moves_list = { 
                'head_left':{'robotSpeech':'Lets go', 'gesture': 'head_left', 'speed': 1.5 },
                'head_right':{'robotSpeech':'Look there', 'gesture': 'head_right', 'speed': 1.5 },
                'head_down':{'robotSpeech':'The coin in the groud', 'gesture': 'head_down', 'speed': 1.5 },
                'head_up':{'robotSpeech':'Prayse the lord', 'gesture': 'head_up', 'speed': 1.5 },
                'wide_arms':{'robotSpeech':'Cross', 'gesture': 'wide_arms', 'speed': 1.5 },
                'hands_open':{'robotSpeech':'Open hand', 'gesture': 'hands_open', 'speed': 1.5 },
                'hands_close':{'robotSpeech':'Close hand', 'gesture': 'hands_close', 'speed': 1.5 }
        }

        # moves = moves_list.keys()

        for move in moves_list.keys():
            
            msg = "Now we gonna perform: " + move 
            userdata.robotSay.publish(msg)
    
            # msg = moves_list[move]['robotSpeech']
            userdata.robotSay.publish(moves_list[move]['robotSpeech'])

            # gesturePlay = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
            # rospy.wait_for_service('/qt_robot/gesture/play')
            # gesturePlay(moves_list[move]['gesture'], moves_list[move]['speed'])
            
            # rospy.loginfo("CURRENT MOVE")
            # rospy.loginfo(moves_list[move]['gesture'])


            for seconds in range(5):
                
                msg = numbers[seconds]
                userdata.robotSay.publish(msg)

                rospy.sleep(1)
            # seconds = seconds + 1
        
            # emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
            # rospy.wait_for_service('/qt_robot/emotion/show')
            # emotionShow('QT/happy')


        # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        # rospy.wait_for_service('/qt_robot/speech/say')
        # speechSay("Great ! The next stretch is moving the head up.")
        
        msg = "Great ! We did it."
        userdata.robotSay.publish(msg)


        return 'proceed'





class IrecheckManager():
    def __init__(self):
        self.world = pd.DataFrame()     # dataframe storing all info of relevance for iReCHeCk (sources: Dynamico)

        # initialize ROS node
        rospy.init_node('irecheckmanager', anonymous=True)
        # initialize subscribers
        rospy.Subscriber('/qt_nuitrack_app/faces', Faces, self.nuitrackCallback)
        # rospy.Subscriber('/qt_nuitrack_app/faces', String, self.fakeNuitrackCallback)
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        rospy.Subscriber('autodecisions', String, self.decisionsCallback)

        # create a SMACH state machine
        self.sm = smach.StateMachine(outcomes=['end'])
        # create and initialize the variables to be passed to states
        self.sm.userdata.faceKey = False
        self.sm.userdata.dynamicoKey = False
        self.sm.userdata.goToActivityKey = False
        self.sm.userdata.goToEndAssessmentKey = False
        self.sm.userdata.moveOnKey = False
        self.sm.userdata.dynamicoAssessmentKey = False
        self.sm.userdata.pubBehMsg = rospy.Publisher('/irecheck/button_name', String, queue_size=1)
        self.sm.userdata.pubCommandMsg = rospy.Publisher('managercommands', String, queue_size=1)

        # I changed the topic so QT moves the mouth while speaking too
        # self.sm.userdata.robotSay = rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)
        #self.sm.userdata.robotSay = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size=1)
        
        
        # Changing here to also fit when the robot is not present
        self.sm.userdata.robotSay = global_robotSay


        # use the initial time as the filename to save the .csv 
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        
        subject_id = str("TESTE") # e.g. ID01
        # subject_id = str(sys.argv[1]) # e.g. ID01
        self.filename = '~/Documents/iReCHeCk_logs/' + dt_string + '_' + subject_id + '.csv'

        rospy.loginfo("Starting IrecheckManager for subject: {}".format(subject_id))
        
        

        with self.sm:
            # Add states to the container
            # smach.StateMachine.add('BREAK', Break(), 
            #                     transitions={'proceed':'ASSESSMENT'},
            #                     remapping={'continueKey':'faceKey',
            #                                 'pubBehMsg':'pubBehMsg',
            #                                 # 'robotSay':'robotSay', 
            #                                 # 'continueKey':'faceKey',
            #                                 # 'pubBehMsg':'pubBehMsg',
            #                                 'robotSay':'robotSay'})

            smach.StateMachine.add('BREAK', Break(), 
                                transitions={'proceed':'ACTIVITY'},
                                # transitions={'proceed':'end'},
                                remapping={'continueKey':'faceKey',
                                            'pubBehMsg':'pubBehMsg',
                                            # 'robotSay':'robotSay', 
                                            # 'continueKey':'faceKey',
                                            # 'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
            
            smach.StateMachine.add('ASSESSMENT', Assessment(), 
                                transitions={'proceed':'ACTIVITY',
                                            'bye': 'GOODBYE'},
                                remapping={'continueKey':'dynamicoAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay',
                                            'pubCommandMsg': 'pubCommandMsg',
                                            'isEndAssessment': 'goToEndAssessmentKey', # TODO: rename the key
                                            'continueKey':'dynamicoAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay',
                                            'pubCommandMsg': 'pubCommandMsg'})

            smach.StateMachine.add('ACTIVITY', Activity(), 
                                transitions={'proceed':'GOODBYE',
                                             'break': 'BREAK',
                                             'getBack': 'ASSESSMENT',
                                             'stay': 'ACTIVITY'},
                                remapping={'continueKey':'moveOnKey',
                                            'getBackKey':'goToEndAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'moveOnKey',
                                            'getBackKey':'goToEndAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
            smach.StateMachine.add('GOODBYE', Goodbye(), 
                                transitions={'proceed':'end'},
                                remapping={'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay',
                                            'pubBehMsg':'pubBehMsg', 
                                            'robotSay':'robotSay'})


        self.sm.set_initial_state(['ASSESSMENT'])
        # self.sm.set_initial_state(['BREAK'])


        rospy.loginfo("Starting SM in 2 secs")
        rospy.sleep(2)

        # execute SMACH plan
        outcome = self.sm.execute()
        rospy.loginfo("OUTCOME: " + outcome)
        # rospy.spin()
 
        return 



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
                                transitions={'proceed':'ACTIVITY',
                                            'bye': 'GOODBYE'},
                                remapping={'continueKey':'dynamicoAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay',
                                            'pubCommandMsg': 'pubCommandMsg',
                                            'isEndAssessment': 'goToEndAssessmentKey', # TODO: rename the key
                                            'continueKey':'dynamicoAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay',
                                            'pubCommandMsg': 'pubCommandMsg'})
            smach.StateMachine.add('ACTIVITY', Activity(), 
                                transitions={'proceed':'GOODBYE',
                                             'getBack': 'ASSESSMENT',
                                             'stay': 'ACTIVITY'},
                                remapping={'continueKey':'moveOnKey',
                                            'getBackKey':'goToEndAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'moveOnKey',
                                            'getBackKey':'goToEndAssessmentKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})
            smach.StateMachine.add('GOODBYE', Goodbye(), 
                                transitions={'proceed':'end'},
                                remapping={'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay',
                                            'pubBehMsg':'pubBehMsg', 
                                            'robotSay':'robotSay'})
        
        self.sm.set_initial_state(['SLEEPING'])

        # execute SMACH plan
        outcome = self.sm.execute()
        rospy.loginfo("OUTCOME: " + outcome)
        rospy.spin()
 
    
    
    # callback on dynamicomsg
    def dynamicoCallback(self, data):
        # log the reception of the message
        # rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        rospy.loginfo(rospy.get_caller_id() + '- received message from dynamico')
        # notify the FSM of the arrival of new dynamico data
        self.sm.userdata.dynamicoKey = True
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')

        dynamicoType = df.at[0, 'type']

        if dynamicoType == 'assessment':
            self.sm.userdata.dynamicoAssessmentKey = True
            self.sm.userdata.dynamicoKey = False
        elif dynamicoType == 'activity':
            self.sm.userdata.dynamicoKey = True
            self.sm.userdata.dynamicoAssessmentKey = False
        else:
            rospy.loginfo("Unknown dynamico type")

        # append the new record to the dataframe
        self.world = self.world.append(df)
        # fill the empty values with the latest known value for that key
        self.world.fillna( method ='ffill', inplace = True)
        self.save2csv()
        # self.shareWorld()


    # callback on nuitrack/faces
    def nuitrackCallback(self, data):
        # log the reception of the message
        #rospy.loginfo(rospy.get_caller_id() + '- received %s', data.faces)
        rospy.loginfo(rospy.get_caller_id() + '- received face')
        # notify the FSM of the detection of a face
        self.sm.userdata.faceKey = True
    
    def fakeNuitrackCallback(self, data):
        # rostopic pub -1 /qt_nuitrack_app/faces std_msgs/String fakeFace
        # only for testing
        rospy.loginfo(rospy.get_caller_id() + '- received face')
        # notify the FSM of the detection of a face
        self.sm.userdata.faceKey = True

    # callback on autodecisions
    def decisionsCallback(self, data):
         # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # notify the FSM of the arrival of new decisions data
        if (data.data == 'moveOn'):
            self.sm.userdata.moveOnKey = True
            self.sm.userdata.goToEndAssessmentKey = False
            self.sm.userdata.goToActivityKey = False

        elif (data.data == 'goToEndAssessment'):
            self.sm.userdata.moveOnKey = False
            self.sm.userdata.goToEndAssessmentKey = True
            self.sm.userdata.goToActivityKey = False

        elif (data.data == 'goToActivity'):
            
            self.sm.userdata.moveOnKey = False
            self.sm.userdata.goToEndAssessmentKey = False
            self.sm.userdata.goToActivityKey = True
        

    # save the world dataFrame in a CSV file at the end of the session
    def save2csv(self):
        
        self.world.to_csv(self.filename, index=False)

    # # save the world dataFrame in a CSV file at the end of the session
    # def shareWorld(self):

    #     print("JSON---------->", self.world.to_json(orient='records'))



#########################################################################
if __name__ == "__main__":
    try:
        myIrecheckManager = IrecheckManager()
    except rospy.ROSInterruptException:
        pass
    finally:
        myIrecheckManager.save2csv()