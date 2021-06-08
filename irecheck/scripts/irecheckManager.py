#!/usr/bin/env python3

import sys
import rospy
import pandas as pd
from std_msgs.msg import String
from numpy.lib.shape_base import split
from datetime import datetime


class IrecheckManager():

    def __init__(self):
        self.world = pd.DataFrame()     # dataframe storing all info of relevance for iReCHeCk (sources: Dynamico)

        # initialize ROS node
        rospy.init_node('irecheckmanager', anonymous=True)
        # initialize publishers/subscribers
        # rospy.Subscriber([topic_name],[topic_type],[callback_function_name])
        rospy.Subscriber('dynamicomsg', String, self.dynamicoCallback)
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])

        # keep python from exiting until this node is stopped
        rospy.spin()

    
    # save the dynamico data on the dataframe
    def dynamicoCallback(self, data):
        # log the reception of the message
        rospy.loginfo(rospy.get_caller_id() + '- received %s', data.data)
        # extract the data in the message and convert it in dataframe format
        df = pd.read_json(data.data, orient='records')
        # # DEBUG ONLY
        # print(df)
        # append the new record to the dataframe
        self.world = self.world.append(df)
        # fill the empty values with the latest known value for that key
        self.world.fillna( method ='ffill', inplace = True)
        # [DEBUG ONLY]
        print(self.world)
    

    # append a new record to the dataframe
    def addRecord(self,newRecord):
        self.world.loc[len(self.world)] = newRecord
        self.latestRow = self.latestRow + 1
        # [DEBUG ONLY]
        print(self.world)
    

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
