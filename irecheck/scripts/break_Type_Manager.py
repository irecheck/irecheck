#!/usr/bin/env python3

 
import rospy
import smach
import pandas as pd
import roslib; roslib.load_manifest('smach')
from std_msgs.msg import String
from qt_nuitrack_app.msg import Faces
from datetime import datetime
import sys
import random

from qt_robot_interface.srv import *
from qt_gesture_controller.srv import gesture_play
from qt_motors_controller.srv import *
from std_msgs.msg import Float64MultiArray



NUM_OF_ROUNDS = 2
# NUM_OF_ROUNDS = 1

BREAK_COUNTER = 0
NUMBER_BREAKS = 1

CONDITION = int(sys.argv[3]) #get the type of condition
CONDITION_OPTIONS = ['breathe', 'stretch']
EXPERIMENT_CONDITION = CONDITION_OPTIONS[CONDITION]

# robot_connected = False
robot_connected = True

CURRENT_ROUND = 0


CONGRATS = ['Great!', 'Awesome!', 'Nice!', 'Excellent!', 'Cool!', 'You rock!', 'Very good!', "Alright!", 'You got it!', 'You are on fire!' ]


class global_robotSay():



    if robot_connected:

        def publish(sentence):
            rospy.loginfo(sentence)
            speechSay = rospy.ServiceProxy('/qt_robot/behavior/talkText', behavior_talk_text)
            # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
            # rospy.wait_for_service('/qt_robot/speech/say')
            rospy.wait_for_service('/qt_robot/behavior/talkText')
            speechSay(sentence)
    
    else:
        
        def publish(sentence):
            rospy.loginfo(sentence)


class Welcome(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['proceed'],
                             input_keys=['continueKey','pubBehMsg','robotSay'],
                             output_keys=['continueKey','pubBehMsg','robotSay'])


    def execute(self, userdata):
        
        rospy.loginfo('Executing state WELCOME')
        # stay here until the condition for transitioning is met
        # while(userdata.continueKey != True):
        #     pass
        
        try:
            subject_name = str(sys.argv[2]) # e.g. Jonas
            rospy.loginfo("\n\nInteraction started for subject named: " + str(subject_name + "\n\n"))

        except:
            rospy.loginfo("\n\nNO child name provided. Calling the poor unamed of <<My friend>>\n\n")
            subject_name="My friend"

        # transition to the next state (react the the event and say a proactive sentence)
        userdata.continueKey = False
        msg = 'bonjour'
        rospy.loginfo(msg)
        userdata.pubBehMsg.publish(msg) 
        
        rospy.sleep(3)


        # msg= "Hey, " + subject_name
        # userdata.robotSay.publish(msg)   

        msg= "Pleased to meet you. I am Q T robot!  I come from  E P F L, in Lôussanne, and I help the children to increase their handwriting skills" 
        userdata.robotSay.publish(msg)   


        msg = "It will be a pleasure to play with you today!"
        # rospy.loginfo(msg)
        userdata.robotSay.publish(msg)   
        # rospy.sleep(1):

        msg = "Let's start by making a first analysis of your handwriting!"
        # rospy.loginfo(msg)
        userdata.robotSay.publish(msg)
        # rospy.sleep(1) 
        
        msg = "Take the pen in front of you!"
        # rospy.loginfo(msg)
        userdata.robotSay.publish(msg)
        rospy.sleep(2) 
        
        msg = "Do you have it?! Great! Now, on the iPad in front of you, check the screen. On the left part, click in the blue button named: New Analysis!"
        # rospy.loginfo(msg)
        userdata.robotSay.publish(msg)
        rospy.sleep(2) 
        

        msg = "You will starting by drawing a cat in the white part. When you finish, click in the green button on the side of the first cat."
        # rospy.loginfo(msg)
        userdata.robotSay.publish(msg)
        rospy.sleep(3) 
        # rospy.sleep(30) 
        
        msg = "When you finish drawing the cat, click in the green button. Then, you will have to copy the text you see in the space below."
        # rospy.loginfo(msg)
        userdata.robotSay.publish(msg)
        rospy.sleep(1) 

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
        
        # msg = "It is time to check how your handwriting is going. You gonna do the " # Please perform an evaluation. It could take a while for me to compute it after you finish."
        # userdata.robotSay.publish(msg)
        # # rospy.loginfo(msg)
       
       
        rospy.sleep(2)


        while(userdata.continueKey != True):
            pass
        
        userdata.continueKey = False
        self.assessment_counter = self.assessment_counter + 1
        rospy.loginfo('Finish {} assessment'.format(self.assessment_counter))
        if self.assessment_counter < NUM_OF_ROUNDS:
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
        
        
            msg = "Yes! You did it. This is the result of your handwriting. Take a time to look at them."
            # rospy.loginfo(msg)
            userdata.robotSay.publish(msg)
            rospy.sleep(5) 

            
            msg = "Let's make them better!. On the top of the screen, you will see your name. Click on it with the pen to come back to the main screen."
            # rospy.loginfo(msg)
            userdata.robotSay.publish(msg)
            rospy.sleep(2) 

            


            msg = "Well Done!, Now, on the right part, click in the blue button named: New Activity! So we can start playing!"
            # rospy.loginfo(msg)
            userdata.robotSay.publish(msg)
            rospy.sleep(2) 


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
            
            userdata.getBackKey = False
            
            # if break didnt happen yet, make a break. Otherwise, send to the last evaluation to finish
            #SHOULD RETHINK IT BETTER LATER (consider the round number here)
            global BREAK_COUNTER
            global NUMBER_BREAKS
            print("------------------------  BREAK_COUNTER", int(BREAK_COUNTER))
            print("NUMBER_BREAKS", NUMBER_BREAKS)
            if BREAK_COUNTER < NUMBER_BREAKS:
                BREAK_COUNTER += 1
                return 'break'
            else:

                msg = "Great! Now, stop! It feels you have been practising enough. Let's check once again your handwriting."
                userdata.robotSay.publish(msg)
                
                msg = "Go back to the handwrite analisys screen. For that, on the top right of the screen, click on the blue button with a X. Then, click on the blue button with a X again and solve the math problem. Ask help to my colleagues to do so."
                userdata.robotSay.publish(msg)
                

                return 'getBack'
            # return 'getBack'
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


        # transition to the next state (end)
        msg = 'au_revoir'
        rospy.loginfo(msg)
        userdata.pubBehMsg.publish(msg)
        # wait some time
       
        msg = "Okay my little friend. This is the end of the session. It was nice to have fun with you!"
        userdata.robotSay.publish(msg)
        # rospy.loginfo(msg)
        # rospy.sleep(1)

        msg = "Bye Bye!"
        userdata.robotSay.publish(msg)


        rospy.sleep(1)   
        return 'proceed'




# --------------------------------- Breaking Classes



class Break(smach.State):
  
    """All the stretching movements."""
    
    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['proceed'],
                            input_keys=['pubBehMsg','robotSay','pubCommandMsg'],
                            output_keys=['pubBehMsg','robotSay','pubCommandMsg'])
        self.say = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
        

    def execute(self, userdata):
  
        if CURRENT_ROUND == NUM_OF_ROUNDS:
            
            
            # msg = "Great! It feels you have been practising enough. Let's check once again your handwriting."
            # userdata.robotSay.publish(msg)
            

            # msg = "Go back to the handwrite analisys screen. Ask help to my colleagues to do so."
            # userdata.robotSay.publish(msg)
            
            return 'proceed'
  


        rospy.loginfo('Starting break session')



        msg = "Ok! We have been playing for a while now. Let's make a pause."
        userdata.robotSay.publish(msg)

        msg = "Please leave the pen on the side of the iPad"
        userdata.robotSay.publish(msg)

        msg = "Do you have your hands free?"
        userdata.robotSay.publish(msg)

        # building the function name
        function_name = "self." + EXPERIMENT_CONDITION + "(userdata)"

        # return the return of the executed function which should be proceed
        ret= eval(function_name)

        msg = 'start_new_round'
        userdata.pubCommandMsg.publish(msg)

        return ret


    def breathe(self, userdata):
        
        rospy.loginfo('Executing breathing state')
        msg = 'Great! We are now going to do some deep breathing !'
        userdata.robotSay.publish(msg)
        gesture = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=1)
        emotion = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=1)
        # gestureService = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
        # rospy.wait_for_service('/qt_robot/gesture/play')
        # rest.call(['left_arm', 'right_arm', 'HeadPitch'])
        rospy.sleep(1.)
        

        # msg = 'Sit straight in your chair.'
        # userdata.robotSay.publish(msg)
        
        gesture.publish('QT/sneezing')
        # gestureService.call('QT/sneezing', .9)


        msg = "Now, sit straith in your chair so we can enjoy our breathing exercise!"
        userdata.robotSay.publish(msg)

        msg = 'When I say: inhale, you bring the air to your langs slowly. When I say exhale, you leave the air go through your mouth'
        userdata.robotSay.publish(msg)
                


        rospy.sleep(1.)


        msg = "Ready? Let's go!"
        userdata.robotSay.publish(msg)


        for i in range(5):
            
            # gestureService.call("QT/sneezing",.9)
            gesture.publish('QT/sneezing')

            rospy.sleep(1)
            msg = "Inhale"
            userdata.robotSay.publish(msg)

            rospy.sleep(2)
            
            msg = "Exhale"
            userdata.robotSay.publish(msg)
            rospy.sleep(2)

            if i == 2:
                msg = "Just two more times!"
                userdata.robotSay.publish(msg)
                rospy.sleep(2)

            # rospy.wait_for_service('/qt_robot/gesture/play')
        
        msg = 'Bravo!'
        userdata.robotSay.publish(msg)

        # Meditation
        msg = "Now, still siting straith, put your hands on your legs and close your eyes!"
        userdata.robotSay.publish(msg)


        msg = "I want you to concentrate and think about: things that make you happy!"
        userdata.robotSay.publish(msg)

        msg = "I will count to 15 in silence! and tell you when we are done. You keep thinking about it and breathing slowly!"
        userdata.robotSay.publish(msg)
        
        msg = "Ready? Let's go!"
        userdata.robotSay.publish(msg)



        # numbers = ['one', 'two', 'three', 'four', 'five']
        
        for i in range(15):
            
            # msg = i
            # userdata.robotSay.publish(msg)
            rospy.sleep(1)
            rospy.loginfo(i)
        
        
        # Meditation
        msg = "Alright! Open your eyes again!"
        userdata.robotSay.publish(msg)

        emotion.publish('QT/breathing_exercise')
        
        msg = "Take again a deep breath like me!"
        userdata.robotSay.publish(msg)

        msg = "Now, I want you to think about your favorite: music. Don't sing it. Only think. I will count to 15 in silence and tell you when it is done. You keep thinking about it and breathing slowly!"
        userdata.robotSay.publish(msg)
        
        msg = "It is the last time. Now go, close your eyes and think about you favorite song and relax!"
        userdata.robotSay.publish(msg)



        # numbers = ['one', 'two', 'three', 'four', 'five']
        
        for i in range(15):
            
            # msg = i
            # userdata.robotSay.publish(msg)
            rospy.sleep(1)
            rospy.loginfo(i)
        
        
        
        
        msg = 'Yes! We did it! Are you rested and feeling calm?!'
        userdata.robotSay.publish(msg)

        userdata.pubBehMsg.publish('bravo')

        msg = 'Cool! I think we are ready to restart the activities again!'
        userdata.robotSay.publish(msg)

        return 'proceed'

    
    def stretch(self, userdata):

        rest = rospy.ServiceProxy('/qt_robot/motors/home', home)
        rospy.wait_for_service('/qt_robot/motors/home')
        rest.call(['left_arm', 'right_arm', 'HeadPitch', 'HeadYaw'])
        # rest.call(['left_arm', 'right_arm', 'HeadPitch'])
       
        msg = 'Excellent! Now we gonna perform a small stretching session'
        userdata.robotSay.publish(msg)


     
        # seconds = 0
        # start_time = time.time()
        # numbers = ['one', 'two', 'three', 'four', 'five']
        numbers = ['one', 'two', 'three', 'four']#, 'five']

        msg = 'Follow my instructions and do as I do. I will count to 4 for each exercise, ok?!'
        userdata.robotSay.publish(msg)
        
        
        headPub = rospy.Publisher('/qt_robot/head_position/command', Float64MultiArray, queue_size=1)
        right_arm_Pub = rospy.Publisher('/qt_robot/right_arm_position/command', Float64MultiArray, queue_size=1)
        left_arm_Pub = rospy.Publisher('/qt_robot/left_arm_position/command', Float64MultiArray, queue_size=1)
        local_speech = rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)
        rospy.sleep(2)#rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)

        headPub.publish(Float64MultiArray(data=[1,0]))


        # Pub1.publish(Float64MultiArray(data=[15, 0, 15]))
        # rospy.sleep(3)
        # Pub2.publish(Float64MultiArray(data=[-20,-85, 0]))
        # rospy.sleep(1)

        def arms_wide():
            right_arm_Pub.publish(Float64MultiArray(data=[15, 0, 15]))
            left_arm_Pub.publish(Float64MultiArray(data=[-15, 0, 15]))
      
        def arms_front():
            # right_arm_Pub.publish(Float64MultiArray(data=[15, 0, 15]))
            # left_arm_Pub.publish(Float64MultiArray(data=[-15, 0, 15]))
            # rospy.sleep(1)
            right_arm_Pub.publish(Float64MultiArray(data=[0, -100, 0]))
            left_arm_Pub.publish(Float64MultiArray(data=[-0,-100, 0]))

        def arms_up():
            right_arm_Pub.publish(Float64MultiArray(data=[80, -70, 10]))
            left_arm_Pub.publish(Float64MultiArray(data=[-80,-70, 10]))
         

        moves_list = { 
                'head_right':{'robotSpeech':'While keeping your trunk straith, look to your right. Just as I am doing.', 'gesture': 'headPub.publish(Float64MultiArray(data=[60,0]))', 'speed': 1.5 },
                'head_left':{'robotSpeech':'Now, to the left.', 'gesture': 'headPub.publish(Float64MultiArray(data=[-60,0]))', 'speed': 1.5 },
                'head_down':{'robotSpeech':'We look down now', 'gesture': 'headPub.publish(Float64MultiArray(data=[-0,30]))', 'speed': 1.5 },
                'head_up':{'robotSpeech':' Next move: Looking up!.', 'gesture': 'headPub.publish(Float64MultiArray(data=[-0,-30]))', 'speed': 1.5 },
                'wide_arms':{'robotSpeech':'Open your arms as wide as you can', 'gesture': 'arms_wide()', 'speed': 1.5 },
                'wide_front':{'robotSpeech':'Now, stretch your arms in front of you', 'gesture': 'arms_front()', 'speed': 1.5 },
                'wide_up':{'robotSpeech':'Now we put our both arms up like this!', 'gesture': 'arms_up()', 'speed': 1.5 },
                
        }

        # moves = moves_list.keys()

        for move in moves_list.keys():
            
            # msg = "Now we gonna perform: " + move 
            # userdata.robotSay.publish(msg)
    
            # msg = moves_list[move]['robotSpeech']
            # userdata.robotSay.publish(moves_list[move]['robotSpeech'])

            # msg = "Do as I am doing and I will count to 5"
            # userdata.robotSay.publish(msg)

            # moves_list[move]['robotSpeech']
            # rospy.sleep(1)
            eval(moves_list[move]['gesture'])
            rospy.sleep(2)
            userdata.robotSay.publish(moves_list[move]['robotSpeech'])
            msg = "Ready? Go!"
            userdata.robotSay.publish(msg)
            

            for seconds in numbers:
                
                # msg = numbers[seconds]
                # msg = numbers[seconds]
                userdata.robotSay.publish(seconds)
                # self.say.publish(msg)
                # rospy.sleep(.2)
            # seconds = seconds + 1


            # emotionShow = rospy.ServiceProxy('/qt_robot/emotion/show', emotion_show)
            # rospy.wait_for_service('/qt_robot/emotion/show')
            # emotionShow('QT/happy')
            
            msg = random.choice(CONGRATS)
            rospy.loginfo(msg)
            local_speech.publish(msg)

            rest = rospy.ServiceProxy('/qt_robot/motors/home', home)
            rospy.wait_for_service('/qt_robot/motors/home')
            rest.call(['left_arm', 'right_arm', 'HeadPitch', 'HeadYaw'])
        

        # speechSay = rospy.ServiceProxy('/qt_robot/speech/say', speech_say)
        # rospy.wait_for_service('/qt_robot/speech/say')
        # speechSay("Great ! The next stretch is moving the head up.")
        
        # msg = "Awesome! We did it."
        msg = "Yes! We did it"
        userdata.robotSay.publish(msg)
        userdata.pubBehMsg.publish('bravo')


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
        # rospy.loginfo("Subscribing")
        # self.sm.userdata.gesturePub = rospy.Publisher('/qt_robot/head_position/command', Float64MultiArray, queue_size=1)

        # rospy.sleep(2)

        # I changed the topic so QT moves the mouth while speaking too
        # self.sm.userdata.robotSay = rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)
        #self.sm.userdata.robotSay = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size=1)
        
        
        # Changing here to also fit when the robot is not present
        self.sm.userdata.robotSay = global_robotSay


        # use the initial time as the filename to save the .csv 
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        
        # subject_id = str("TESTE") # e.g. ID01

        subject_id = str(sys.argv[1]) # e.g. ID01
        self.filename = '~/Documents/iReCHeCk_logs/' + dt_string + '_' + subject_id + '.csv'

        rospy.loginfo("Starting IrecheckManager for subject: {}".format(subject_id))
        
        

        with self.sm:
            # Add states to the container
            smach.StateMachine.add('WELCOME', Welcome(), 
                                transitions={'proceed':'ASSESSMENT'},
                                # transitions={'proceed':'end'},
                                remapping={'continueKey':'faceKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay', 
                                            'continueKey':'faceKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'robotSay':'robotSay'})

            smach.StateMachine.add('BREAK', Break(), 
                                transitions={'proceed':'ACTIVITY'},
                                # transitions={'proceed':'end'},
                                remapping={'continueKey':'faceKey',
                                            'pubBehMsg':'pubBehMsg',
                                            # 'robotSay':'robotSay', 
                                            # 'continueKey':'faceKey',
                                            'pubBehMsg':'pubBehMsg',
                                            'pubCommandMsg': 'pubCommandMsg',
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


        self.sm.set_initial_state(['WELCOME'])
        # self.sm.set_initial_state(['ASSESSMENT'])
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