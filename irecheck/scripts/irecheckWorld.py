#!/usr/bin/env python

import pandas as pd
from datetime import datetime


class IrecheckWorld():
    def __init__(self,brainFields,dynamicoFields,mmaFields,initBrainValues,initDynamicoValues,initMMAValues):
        self.world = pd.DataFrame()     # dataframe storing all info of relevance for iReCHeCk (sources: Dynamico, Multimodal-Analyzer, self...)
        self.latestRow = -1             # index of the latest row inserted in the dataframe
        self.commands = []              # list of commands triggered by the latest analysis on the dataframe

        # # [DEBUG ONLY]
        # print(dynamicoFields)
        # print(initDynamicoValues)
        # print(mmaFields)
        # print(initMMAValues)

        # initialize the dataframe columns with the dynamico fields + the multimodal analyzer fields
        fields = brainFields + dynamicoFields + mmaFields
        self.world = self.world.reindex(self.world.columns.union(fields), axis=1)
        # [DEBUG ONLY]
        print(self.world)
    

    # append a new record to the dataframe
    def addRecord(self,newRecord):
        self.world.loc[len(self.world)] = newRecord
        self.latestRow = self.latestRow + 1
        # [DEBUG ONLY]
        print(self.world)


    # analyse the latest values and return the corresponding commands
    def analyse(self):
        #clean the list of triggered commands
        self.commands = []
        # call the analysis functions related to dynamico data
        self.gameResultReaction()
        self.activityRecommendation()
        # return the list of triggered commands
        return self.commands


    # define the robot's reaction to a game result
    def gameResultReaction(self):
        if (self.world.get_value(self.latestRow,'result') == "w"):
            self.commands.append("autoWIN")
            print("triggered command: autoWIN")
        elif (self.world.get_value(self.latestRow,'result') == "f"):
            self.commands.append("autoLOSS")
            print("triggered command: autoLOSS")
        else:
            pass
    

    # define the robot's recommendation for the next activity
    def activityRecommendation(self):
        # if the user won at a game and it's not highest difficulty, suggest to play the same game with increased difficulty
        if (self.world.get_value(self.latestRow,'result') == "w") and (self.world.get_value(self.latestRow,'level') != "5"):
            suggestion = "nextGame " + self.world.get_value(self.latestRow,'activity') + " " + str(int(self.world.get_value(self.latestRow,'level'))+1)
            self.commands.append(suggestion)
            print("triggered command: " + suggestion)
        # if the user won at a game and it's highest difficulty, suggest to do a test
        elif (self.world.get_value(self.latestRow,'result') == "w") and (self.world.get_value(self.latestRow,'level') == "5"):
            suggestion = "nextGame test"
            self.commands.append(suggestion)
            print("triggered command: " + suggestion)
        # if the user lost at a game and it's not lowest difficulty, suggest to play the same game with decreased difficulty
        elif (self.world.get_value(self.latestRow,'result') == "f") and (self.world.get_value(self.latestRow,'level') != "1"):
            suggestion = "nextGame " + self.world.get_value(self.latestRow,'activity') + " " + str(int(self.world.get_value(self.latestRow,'level'))-1)
            self.commands.append(suggestion)
            print("triggered command: " + suggestion)
        # if the user lost at a game and it's lowest difficulty, suggest to do a test
        elif (self.world.get_value(self.latestRow,'result') == "f") and (self.world.get_value(self.latestRow,'level') == "1"):
            suggestion = "nextGame test"
            self.commands.append(suggestion)
            print("triggered command: " + suggestion)

    
    # save the world dataFrame in a CSV file at the end of the session
    def save2csv(self):
        # backup the dataframe as a CSV file (use current date and time for the file name)
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        filename = '~/Documents/iReCHeCk_logs/' + dt_string + '.csv'
        self.world.to_csv(filename)