#!/usr/bin/env python3

import rospy
import pandas as pd
from std_msgs.msg import String



class DecisionMaker():
    def __init__(self):
        # initialize ROS node
        rospy.init_node('decisionmaker', anonymous=True)
        # initialize publishers/subscribers
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        self.pubFSMMsg = rospy.Publisher('autodecisions', String, queue_size=10)
        self.pubBehMsg = rospy.Publisher('/irecheck/button_name', String, queue_size=1)
        self.pubSayMsg = rospy.Publisher('/qt_robot/speech/say', String, queue_size=1)

        # keep python from exiting until this node is stopped
        rospy.spin()
     
    # callback on dynamicomsg
    def dynamicoCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')
        # DEBUG ONLY
        print(df)

        # implement a simple logic to determine what to suggest next
        # if ASSESSMENT --> suggest the activity associated with the lowest score, move to ACTIVITY state
        if (df.at[0, 'type'] == 'assessment'):
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
            msg = 'goToActivity'
            rospy.loginfo(msg)
            self.pubFSMMsg.publish(msg)  
        # if ACTIVITY
        #   if the score in the current game is above 50 --> congratulations, move to GOODBYE state
        #   else --> encouragement and try again
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


#########################################################################
if __name__ == "__main__":
    try:
        myDecisionMaker = DecisionMaker()
    except rospy.ROSInterruptException:
        pass
