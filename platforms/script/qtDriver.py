#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from random import randint
import sys
import mysql.connector
from mysql.connector import Error
from irecheck.srv import *
from std_msgs.msg import Float64MultiArray

class QTRobot():
    #global languagec
    def __init__(self):
	global message 
	message = "idle"

            # initialize ROS node
        rospy.init_node('qtdriver', anonymous=True)
        # initialize publishers/subscribers.
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])
        self.pub_say = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size=10)
	self.pub_emotion = rospy.Publisher('qt_robot/emotion/show', String, queue_size=10)
	self.pub_gesture = rospy.Publisher('qt_robot/gesture/play', String, queue_size=10)
            # create emotion publisher
        self.emotion_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=1)

	while True:
            # rospy.Subscriber([topic_name],[topic_type],[callback_function_name])
            rospy.Subscriber('robotcommandcopy', String, self.coreengineCallbackrobot)
            rospy.Subscriber('language', String, self.languageCall)
            rospy.Subscriber('gamerecommendation', String, self.MLCallback)
	    if (message == "idle"):
	        self.coreengineCallbackrobotidle(message)
	    else:
	        pass




        # keep python from exiting until this node is stopped
            rospy.spin()
    def languageCall(self, data):
        # log the reception of the message
	global languagec
        languagec = data.data
        rospy.loginfo(rospy.get_caller_id() + '- received %s', languagec)

    def MLCallback(self, data):
        # log the reception of the message
	global gamerec
	global levelrec
	global username
        messagegame = data.data
        rospy.loginfo(rospy.get_caller_id() + '- received %s', messagegame)
        # parse the message to get the values
        self.brainmsg = messagegame.strip().split()
	if ((self.brainmsg [0] == "TILT" or self.brainmsg [0] == "STATIC" or self.brainmsg [0] == "KINEMATIC" or self.brainmsg [0] == "PRESSURE") and (self.brainmsg [1] == "1" or self.brainmsg [1] == "2" or self.brainmsg [1] == "3" or self.brainmsg [1] == "4" or self.brainmsg [1] == "5")):
            gamerec = self.brainmsg [0]
	    levelrec = int(self.brainmsg [1])
	    username = self.brainmsg [2]
	    

    def coreengineCallbackrobot(self, data):
        # log the reception of the message
	global message
        message = data.data
        rospy.loginfo(rospy.get_caller_id() + '- received %s', message)
	#return message
	Randmsg = randint (1,11)
        Randemotion = randint(1,9)
	#Randmsg = 1

	if (message == "robotWIN"):

	    if (languagec == "French"):
	        #self.pub_emotion.publish("QT/talking")
	        if (Randmsg == 1):
                    self.pub_say.publish("Bien joue! Tu as gagne. Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Bien joue! Tu as gagne. Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 2):
                    self.pub_say.publish("Tu as reussi le jeu! Felicitations! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Tu as reussi le jeu! Felicitations! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 3):
                    self.pub_say.publish("Tu as reussi ! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Tu as reussi ! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 4):
                    self.pub_say.publish("Bien joue, tu as reussi! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Bien joue, tu as reussi! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 5):
                    self.pub_say.publish("Felicitations, bien trouve! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Felicitations, bien trouve! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 6):
                    self.pub_say.publish("ca y est! Tu as reussi! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("ca y est! Tu as reussi! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 7):
                    self.pub_say.publish("Tu es le meilleur! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Tu es le meilleur! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 8):
                    self.pub_say.publish("Bien joue champion. Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Bien joue champion. Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 9):
                    self.pub_say.publish("Wow, tu es le meilleur. Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Wow, tu es le meilleur. Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        else:
                    self.pub_say.publish("Woaaaw! Tu as reussi! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Woaaaw! Tu as reussi! Joue %s niveau %d %s"  % (gamerec, levelrec, username))


	    else:
	        #self.pub_emotion.publish("QT/talking")
	        if (Randmsg == 1):
                    self.pub_say.publish("Congrats! You win. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Congrats! You win. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 2):
                    self.pub_say.publish("You won the game, congratulations! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("You won the game, congratulations! Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 3):
                    self.pub_say.publish("You are the winner! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("You are the winner! Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 4):
                    self.pub_say.publish("Good job! you win. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Good job! you win. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 5):
                    self.pub_say.publish("Congrats! nice try. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Congrats! nice try. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 6):
                    self.pub_say.publish("That's it! You win. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("That's it! You win. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 7):
                    self.pub_say.publish("You are the best! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("You are the best! Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 8):
                    self.pub_say.publish("Well done! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Well done! Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 9):
                    self.pub_say.publish("well! You are the best! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("well! You are the best! Play %s level %d %s" % (gamerec, levelrec, username))

	        else:
                    self.pub_say.publish("Wow! You won the game! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Wow! You won the game! Play %s level %d %s" % (gamerec, levelrec, username))

		rospy.sleep(2)
	    if (Randemotion == 1):
	        self.pub_emotion.publish("QT/happy")

	    elif (Randemotion == 2):
	        self.pub_gesture.publish("QT/happy")

	    elif (Randemotion == 3):
	        self.pub_emotion.publish("QT/happy")
	        self.pub_gesture.publish("QT/happy")

	    elif (Randemotion == 4):
	        self.pub_emotion.publish("QT/kiss")
	        self.pub_gesture.publish("QT/kiss")

	    elif (Randemotion == 5):
	        self.pub_emotion.publish("QT/kiss2")
	        self.pub_gesture.publish("QT/send_kiss")

	    elif (Randemotion == 6):
	        self.pub_emotion.publish("QT/one_eye_wink")
	        self.pub_gesture.publish("QT/challenge")

	    elif (Randemotion == 7):
	        self.pub_emotion.publish("QT/showing_smile")
	        self.pub_gesture.publish("QT/happy")

	    elif (Randemotion == 8):
	        self.pub_emotion.publish("QT/surprise")
	        self.pub_gesture.publish("QT/surprise")


	    else:
	        pass








	elif (message == "robotLOSS"):
	    if (languagec == "French"):

	        if (Randmsg == 1 ):
                    self.pub_say.publish("Essaie encore! Tu fais du bon boulot! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Essaie encore! Tu fais du bon boulot! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 2):
                    self.pub_say.publish("Ce nest pas grave si tu ne reussis pas du premier coup, continue! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Ce nest pas grave si tu ne reussis pas du premier coup, continue! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 3):
                    self.pub_say.publish("On ne peut gagner sans apprendre a perdre d\'abord. Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("On ne peut gagner sans apprendre a perdre d\'abord. Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 4):
                    self.pub_say.publish("Tu as rate, essaie encore, et fais de ton mieux. Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Tu as rate, essaie encore, et fais de ton mieux. Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 5):
                    self.pub_say.publish("Ce n\'est pas grave si tu n'as pas reussi, essaie juste de t\'ameliorer! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Ce n\'est pas grave si tu n'as pas reussi, essaie juste de t\'ameliorer! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 6 ):
                    self.pub_say.publish("Essaie encore, ce n'est pas le moment d'abandonner! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Essaie encore, ce n'est pas le moment d'abandonner! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 7 ):
                    self.pub_say.publish("Je t'applaudis pour tes efforts, essaie encore une fois! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Je t'applaudis pour tes efforts, essaie encore une fois! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 8 ):
                    self.pub_say.publish("Essaie encore une fois, tu reussiras la prochaine fois! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Essaie encore une fois, tu reussiras la prochaine fois! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        elif (Randmsg == 9 ):
                    self.pub_say.publish("Tu peux de nouveau essayer! Ne t'inquiete pas et souris! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Tu peux de nouveau essayer! Ne t'inquiete pas et souris! Joue %s niveau %d %s"  % (gamerec, levelrec, username))

	        else:
                    self.pub_say.publish("Ne sois pas triste, et reessaie! Joue %s niveau %d %s"  % (gamerec, levelrec, username))
                    rospy.loginfo("Ne sois pas triste, et reessaie! Joue %s niveau %d %s"  % (gamerec, levelrec, username))



	    else:

	        if (Randmsg == 1 ):
                    self.pub_say.publish("You need to try again. good job! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("You need to try again. good job! Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 2):
                    self.pub_say.publish("Winning isn't everything, but wanting it is. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Winning isn't everything, but wanting it is. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 3):
                    self.pub_say.publish("You can't win unless you learn how to lose. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("You can't win unless you learn how to lose. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 4):
                    self.pub_say.publish("You failed but no matter. Just try to get better. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("You failed but no matter. Just try to get better. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 5):
                    self.pub_say.publish("You failed! try again and do your best. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("You failed! try again and do your best. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 6 ):
                    self.pub_say.publish("Try again. It is not the time to lose! Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Try again. It is not the time to lose! Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 7 ):
                    self.pub_say.publish("I applaud your try. You can try again. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("I applaud your try. You can try again. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 8 ):
                    self.pub_say.publish("Try again. Next time you win. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Try again. Next time you win. Play %s level %d %s" % (gamerec, levelrec, username))

	        elif (Randmsg == 9 ):
                    self.pub_say.publish("You can try again. Don't worry be happy! Play %s"%messagegame)
                    rospy.loginfo("You can try again. Don't worry be happy! Play %s"%messagegame)

	        else:
                    self.pub_say.publish("Don't be sad. Make another try. Play %s level %d %s" % (gamerec, levelrec, username))
                    rospy.loginfo("Don't be sad. Make another try. Play %s level %d %s" % (gamerec, levelrec, username))

		rospy.sleep(2)
	    if (Randemotion == 1 or 2 or 3 or 4):
	        self.pub_emotion.publish("QT/sad")

	    else:
		pass
	rospy.sleep(8)
        message = "idle"

	#self.coreengineCallbackrobotidle(message)




##############################
### idle function
    def coreengineCallbackrobotidle(self, message):
        # create head publisher
        head_pub = rospy.Publisher('/qt_robot/head_position/command', Float64MultiArray, queue_size=1)

        # create emotion publisher
        emotion_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=1)

        # create emotion publisher
        gesture_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=1)


        right_pub = rospy.Publisher('/qt_robot/right_arm_position/command', Float64MultiArray, queue_size=1)

        left_pub = rospy.Publisher('/qt_robot/left_arm_position/command', Float64MultiArray, queue_size=1)


        # wait for publisher connections
        wtime_begin = rospy.get_time()
        while (head_pub.get_num_connections() == 0 or emotion_pub.get_num_connections() == 0 or gesture_pub.get_num_connections() == 0 or right_pub.get_num_connections() == 0 or left_pub.get_num_connections() == 0) :
            rospy.loginfo("waiting for publisher connections...")
            if rospy.get_time() - wtime_begin > 10.0:
                rospy.logerr("Timeout while waiting for publisher connection!")
                sys.exit()
            rospy.sleep(1)



    
        # log the reception of the message
        #message = data.data
        # centering the head
	#message = 'idle'
        href = Float64MultiArray(data=[0,0])
        head_pub.publish(href)
        rospy.sleep(1)


        refr = Float64MultiArray()
        refl = Float64MultiArray()
        ShoulderPitchDefault = 90
        ShoulderRollDefault = -60
        ElbowRollDefault = -30
        while message == 'idle':
	    # head movement
	    num = randint (1,4)
	    for i in range (num):
                mic = randint (-10, 10)
                angle = randint (-40, 40)
                rospy.loginfo("up and down: %d , turning: %d" % (mic, angle))
                href.data = [angle, mic]
                head_pub.publish(href)
	        rospy.sleep(2)
	


	    # emotions and gestures
	    emotionRand = randint (1,55)
	    #emotionRand = 41
	    if (emotionRand == 1):
	        emotion_pub.publish("QT/with_a_cold")
                rospy.loginfo("emotion: with_a_cold")

	    elif (emotionRand == 3):
	        emotion_pub.publish("QT/yawn")
	        gesture_pub.publish("QT/yawn")
                rospy.loginfo("emotion: yawn , gesture: yawn")

    	    elif (emotionRand == 5):
    	        emotion_pub.publish("QT/with_a_cold_sneezing")
    	        gesture_pub.publish("QT/sneezing")
                rospy.loginfo("emotion: with_a_cold_sneezing , gesture: sneezing")

	    elif (emotionRand == 7):
	        emotion_pub.publish("QT/confused")
                rospy.loginfo("emotion: confused")

	    elif (emotionRand == 9):
	        emotion_pub.publish("QT/puffing_the_chredo_eeks")
                rospy.loginfo("emotion: puffing_the_chredo_eeks")

	    elif (emotionRand == 11):
	        emotion_pub.publish("QT/showing_smile")
                rospy.loginfo("emotion: showing_smile")

	    elif (emotionRand == 13):
	        emotion_pub.publish("QT/blowing_raspberry")
                rospy.loginfo("emotion: blowing_raspberry")

	    elif (emotionRand == 15):
	        emotion_pub.publish("QT/brushing_teeth")
                rospy.loginfo("emotion: brushing_teeth")

	    elif (emotionRand == 17):
	        emotion_pub.publish("QT/happy_blinking")
                rospy.loginfo("emotion: happy_blinking")

	    elif (emotionRand == 19):
	        emotion_pub.publish("QT/surprise")
                rospy.loginfo("emotion: surprise")

	    elif (emotionRand == 21):
	        emotion_pub.publish("QT/one_eye_wink")
                rospy.loginfo("emotion: one_eye_wink")

	    elif (emotionRand == 23):
	        emotion_pub.publish("QT/breathing_exercise")
	        gesture_pub.publish("QT/breathing_exercise")
                rospy.loginfo("emotion: breathing_exercise , gesture: breathing_exercise")

	    elif (emotionRand == 25):
	        emotion_pub.publish("QT/brushing_teeth_foam")
                rospy.loginfo("emotion: brushing_teeth_foam")

	    #elif (emotionRand == 27):
	        #emotion_pub.publish("QT/calmig_down_exercise_nose")
	        #gesture_pub.publish("QT/breathing_exercise")
                #rospy.loginfo("emotion: calmig_down_exercise_nose , gesture: breathing_exercise")

	    elif (emotionRand == 29):
	        emotion_pub.publish("QT/calming_down")
                rospy.loginfo("emotion: calming_down")

	    elif (emotionRand == 31):
	        gesture_pub.publish("QT/bored")
                rospy.loginfo("emotion: bored")

	    elif (emotionRand == 33):
	        emotion_pub.publish("QT/kiss2")
                rospy.loginfo("emotion: kiss2")

	    elif (emotionRand == 35):
	        emotion_pub.publish("QT/dirty_face")
	        rospy.sleep(3)
	        emotion_pub.publish("QT/dirty_face_wash")
                rospy.loginfo("emotion: dirty_face_wash")

	    elif (emotionRand == 37):
	        emotion_pub.publish("QT/dirty_face_sad")
	        rospy.sleep(3)
	        emotion_pub.publish("QT/dirty_face_wash")
                rospy.loginfo("emotion: dirty_face_sad_wash")

	    elif (emotionRand == 39):
	        emotion_pub.publish("QT/with_a_cold_cleaning_nose")
	        gesture_pub.publish("QT/sneezing")
                rospy.loginfo("emotion: with_a_cold_cleaning_nose , gesture: sneezing")

	    elif (emotionRand == 41):
                ShoulderRoll = ShoulderRollDefault+20
                refr.data = [-ShoulderPitchDefault, ShoulderRoll, ElbowRollDefault]
                refl.data = [ShoulderPitchDefault, ShoulderRoll, ElbowRollDefault]
                right_pub.publish(refr)
                left_pub.publish(refl)
	        rospy.sleep(0.5)


                ShoulderPitchr = -ShoulderPitchDefault +50
                ShoulderPitchl = ShoulderPitchDefault -50
                ShoulderRoll = ShoulderRollDefault -40
                ElbowRoll = ElbowRollDefault -35
                rospy.loginfo("RightShoulderPitch: %d , RightShoulderRoll: %d , RightElbowRoll:%d" % (ShoulderPitchr, ShoulderRoll, ElbowRoll))
                rospy.loginfo("LeftShoulderPitch: %d , LeftShoulderRoll: %d , LeftElbowRoll:%d" % (ShoulderPitchl, ShoulderRoll, ElbowRoll))
                refr.data = [ShoulderPitchr, ShoulderRoll, ElbowRoll]
                refl.data = [ShoulderPitchl, ShoulderRoll, ElbowRoll]
                right_pub.publish(refr)
                left_pub.publish(refl)
	        rospy.sleep(0.5)


	    else:
	        pass

	    rospy.sleep(3)

	    # arm movements
	    num = randint(1,2)
	    for i in range (num):
	        ShoulderRand = randint (-10,10)
                ShoulderPitchr = -ShoulderPitchDefault - ShoulderRand
                ShoulderPitchl = ShoulderPitchDefault + ShoulderRand
                ShoulderRoll = ShoulderRollDefault + randint (-20,20)
                ElbowRoll = ElbowRollDefault + randint (-10,10)
                rospy.loginfo("RightShoulderPitch: %d , RightShoulderRoll: %d , RightElbowRoll:%d" % (ShoulderPitchr, ShoulderRoll, ElbowRoll))
                rospy.loginfo("LeftShoulderPitch: %d , LeftShoulderRoll: %d , LeftElbowRoll:%d" % (ShoulderPitchl, ShoulderRoll, ElbowRoll))
                refr.data = [ShoulderPitchr, ShoulderRoll, ElbowRoll]
                refl.data = [ShoulderPitchl, ShoulderRoll, ElbowRoll]
                right_pub.publish(refr)
                left_pub.publish(refl)
	        rospy.sleep(3)


        rospy.loginfo("shutdowned!")


if __name__ == '__main__':
    try:

	#languagec = "French"
        r = QTRobot()
    except rospy.ROSInterruptException:
        pass
