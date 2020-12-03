#!/usr/bin/env python

import mysql.connector
from mysql.connector import Error
import rospy
from std_msgs.msg import String
from irecheck.srv import DynamicoFieldsSrv,DynamicoFieldsSrvResponse


class DynamicoListener():
    def __init__(self):
        # initialize ROS node
        rospy.init_node('dynamicolistener', anonymous=True)
        # initialize publishers/subscribers.
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])
        self.pubMsg = rospy.Publisher('dynamicomsg', String, queue_size=10)
        # initialize services (server)
        # rospy.Service([service_name],[service_type],[handler])
        self.servFields = rospy.Service('sendDynamicoFields', DynamicoFieldsSrv, self.sendDynamicoFieldsHandler)
        rospy.loginfo("Started sendDynamicoFields service")
        # initialize the id of the last record read
        self.lastID = 0

        # set a looping rate of 10 Hz
        self.rate = rospy.Rate(10) # 10hz
    

    # handler for the service of sending the Dynamico field names
    def sendDynamicoFieldsHandler(self, req):
        # connect to the fakedynamico database (assumed to be located in the same computer)
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='fakedynamico',
                                                 user='dynamico',
                                                 password='dynamicopw')
            if connection.is_connected():
                cursor = connection.cursor()
                # fetch the field names
                sql_command = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'dynamico_table'"
                cursor.execute(sql_command)
                records = cursor.fetchall()
                ros_response = ""
                for row in records:
                    ros_response = ros_response + " " + str(row[3])
                # [DEBUG ONLY]
                print(ros_response)
                # provide the fields as response
                response = DynamicoFieldsSrvResponse()
                response.fields = ros_response
                return response

        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                # # [DEBUG ONLY]
                # print("MySQL connection is closed")


    # fetch and publish the latest record from the iReCHeCk database
    def publishLatest(self):
        while not rospy.is_shutdown():
            # connect to the fakedynamico database (assumed to be located in the same computer)
            # this requires mySQL and mySQL-connector-python installed. See:
            # https://pynative.com/python-mysql-database-connection/
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='fakedynamico',
                                                     user='dynamico',
                                                     password='dynamicopw')
                if connection.is_connected():
                    db_Info = connection.get_server_info()
                    cursor = connection.cursor()
                    cursor.execute("select database();")
                    record = cursor.fetchone()
                    # # [DEBUG ONLY]
                    # print("Connected to MySQL Server version ", db_Info)
                    # print("You're connected to database: ", record)
                
                    # fetch the latest record from the DB
                    latestRecord = None
                    sql_command = "SELECT * FROM dynamico_table ORDER BY id DESC LIMIT 1"
                    cursor.execute(sql_command)
                    latestRecord = cursor.fetchone()

                    # publish the record if it's new
                    if (latestRecord != None) and (latestRecord[0] > self.lastID):
                        print("New record found: ", latestRecord)
                        # convert the record into a string (define separator)
                        separator = ' '
                        ros_message = separator.join(map(str, latestRecord))
                        # print the message to screen, on the node's log file and on rosout
                        rospy.loginfo(ros_message)
                        self.pubMsg.publish(ros_message)
                        self.lastID = latestRecord[0]

                # sleep to keep the target execution rate
                self.rate.sleep() 

            except Error as e:
                print("Error while connecting to MySQL", e)

            finally:
                if (connection.is_connected()):
                    cursor.close()
                    connection.close()
                    # # [DEBUG ONLY]
                    # print("MySQL connection is closed")    


#########################################################################
if __name__ == '__main__':
    try:
        myDynamicoListener = DynamicoListener()
        myDynamicoListener.publishLatest()
    except rospy.ROSInterruptException:
        pass