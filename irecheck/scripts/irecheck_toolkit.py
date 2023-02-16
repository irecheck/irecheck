#!/usr/bin/env python3

import time
import pandas as pd
from datetime import datetime
import numpy as np
import rospy
import rosnode
# rosnode.get_node_names()
# id = str(123)
# break_tpye = 'breathe'
# now = datetime.now()
# date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def node_exists(node_name):
    node_list = rosnode.get_node_names()
    return node_name in node_list

def wait_for_node(node_name):
    while not node_exists(node_name):
        # rospy.logwarn("Waiting for node <<{}>> to start...".format(node_name))
        # msg = ("Waiting for node <<{}>> to start...".format(node_name))
        # 
        # for i in range(3):
            # print(msg + i*"... ", end="\r")
        rospy.sleep(1)

class Time_logger():

    def __init__(self, filename, id, name, date, condition):
        
        # print('Logger created for file'+ filename)    
        self.df = pd.read_csv(filename)
        self.id = id
        self.date = date
        self.filename = filename
        self.df = self.df.append({"subject_id":id, "name":name, "condition":condition, "date":date},ignore_index=True)#, ignore=True)


        # print('DF at the moment:\n', self.df)    

    
    def check_keys(self):
                    
        if self.df.subject_id == self.id and self.df.date == self.date:
            return 1
        else:
            return 0

    def add(self, key, value=None):
                    
        # self.df[key] = self.df.apply(self.check_keys())
        if value is not None:
            self.df.loc[self.df.date == self.date, key] = value

        else:
            self.df.loc[self.df.date == self.date, key] = datetime.now().strftime("%H-%M-%S")

        self.df.to_csv(self.filename, index=False)









def lab():


    filename = '~/Documents/iReCHeCk_logs/Sessions_length.csv'

    # file = pd.read_csv(filename)

    # file.at['subject_id']

    # file = file.append({"subject_id":id, "date":date},ignore_index=True)#, ignore=True)

    logger = Time_logger(filename, id, "Teste", "teste", "break_tpye")

    # now = datetime.now()
    timestamp = datetime.now().strftime("%H-%M-%S")

    logger.add('started', timestamp)

    time.sleep(5)

    timestamp = datetime.now().strftime("%H-%M-%S")
    logger.add('ended')


    print(logger.df)

    # file = file.append({"started":timestamp},ignore_index=True)

    # file.loc[file.date == date, 'started'] = timestamp


    # file.to_csv(filename, index=False)

    # print(file)



if __name__ == '__main__':
    lab()