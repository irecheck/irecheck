#!/usr/bin/env python3

# from datetime import time
import time

from numpy import record
import rospy
from std_msgs.msg import String
import pandas as pd


class FakeDynamico():

    def __init__(self):
        rospy.init_node('talker', anonymous=True)
        self.pub = rospy.Publisher('dynamicomsg', String, queue_size=1)
        self.dataframe = pd.read_csv("/home/chenwang/Downloads/14-09-2021_15-13-13.csv")
        # self.dataframe = pd.read_csv("/home/chenwang/Documents/iReCHeCk_logs/03-11-2021_16-32-11-dryrun-daniel-fake.csv")
        # print(self.dataframe)
        self.id = 0

    # publish fake dynamicomsg with a fixed frequency
    def talker(self):
        toggle = 0
        rate = rospy.Rate(1) # 1hz
        typed = ''
        while 1:
            # if (toggle == 0):
        
            typed = input("Just press enter or type fakeAct/fakeEva:")
            
            if typed == 'q':
                break
            elif typed == 'fakeAct':
                self.sendFakeActivity()
                continue
            elif typed == 'fakeEva':
                self.sendFakeAssessment()
                continue
            
            try:
            # hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"%s","score":72,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'%(time.time())
                line = self.dataframe.iloc[self.id].to_json()
            except:
                rospy.loginfo("Dataframe is over!")
                break

            # print("LINEE", line)
            
            # hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"%s","score":72,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'%(time.time())
            hello_str = '[%s]'%(line)
                    # toggle =1
                # else:
                    # hello_str = '[{"updatedAt":1621435616565,"countryCode":"FR","avatar":"default","birthMonth":9,"birthYear":2007,"createdAt":"2021-5-19 14:46:56","handedness":"left","userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","gender":"female","languageCode":"EN","displayName":"Girl left."}]'
                    # toggle = 0
            rospy.loginfo("Publishing  " + hello_str)
            self.pub.publish(hello_str)
            
            self.id += 1
            
    # publish ONE dynamicomsg
    def talkerOnce(self):
        toggle = 0
        # rospy.init_node('talkerOnce', anonymous=True)
        # pub = rospy.Publisher('dynamicomsg', String, queue_size=10)
        hello_str = '[{"userId":"QtT0sFPO89aasSW7W9vfqHXdvue2","createdAt":"2021-6-3 9:56:10","score":72,"childId":"75DA34CC-64C4-40C5-8639-6653FBF26FDA","level":"PP_04","stars":1,"game":"pursuit"}]'
        rospy.loginfo(hello_str)
        self.pub.publish(hello_str)

    def sendFakeAssessment(self):
        hello_str = '[{"userId":"NONE","childId":"NONE","tiltScoreLabel":"NONE","staticScore":0.1018559919,"aiVersion":8.1,"totalScore":0.1400440243,"createdAt":"NONE","totalScoreLabel":"very_severe","pressureScoreLabel":"severe","pressureScore":0.2182620584,"tiltScore":0.5987449244,"staticScoreLabel":"very_severe","kinematicScore":0.2612010354,"writingAnalysisExerciseId":"NONE","kinematicScoreLabel":"medium","p_d1_ori_peaksPerSec":5.997496846e-30,"car_d0_ori_COHrectangularity":0.8575108264,"p_d0_ori_n5":1.535144776e-78,"rho_d2_wav_60_120_n95":0.0117960247,"az_d1_freq_90bandwidth":0.9773313674,"rho_d2_ori_entropy":0.7782611836,"al_d1_wav_15_30_n5":0.9999998326,"dst_d1_wav_60_120_n5":1.0,"az_d1_wav_15_30_n5":1.0,"p_d1_freq_bin80Hz":0.9638099278,"p_d1_ori_entropy":2.996763377e-45,"al_d1_wav_7_15_n5":0.4667188114,"car_d0_ori_COHperimeter":0.0,"al_d1_ori_n95":0.9529841373,"dst_d1_freq_PSTcorrelation":0.0005577038,"car_d0_ori_PCAlenFirstPA":0.0,"rho_d2_wav_15_30_n95":0.000842446,"car_d0_ori_GENinAirTime":2.269968046e-25,"tht_d1_ori_mean":0.9941053994,"tht_d2_ori_mean":0.8679867407,"p_d1_freq_PSTdiff":2.887185886e-42,"car_d0_ori_GENdensityMean":7.487611282e-36,"az_d1_wav_15_30_n95":0.5062789638,"type":"assessment","level":null,"stars":null,"game":null,"score":null}]'
        rospy.sleep(2) # ROS takes some time to notify the publishers and subscribers of the topics.
        rospy.loginfo(hello_str)
        self.pub.publish(hello_str)

    def sendFakeActivity(self):
        hello_str = '[{"userId":"NONE","createdAt":"NONE","score":100,"childId":"NONE","level":"NONE","stars":3,"game":"pursuit","type":"activity"}]'
        rospy.sleep(2) # ROS takes some time to notify the publishers and subscribers of the topics.
        rospy.loginfo(hello_str)
        self.pub.publish(hello_str)

if __name__ == '__main__':
    try:
        fd = FakeDynamico()
        fd.talker()
        # talkerOnce()
        # talker()
    except rospy.ROSInterruptException:
        pass