#!/usr/bin/env python3

import rospy
import json
import requests
import threading
import pandas as pd

from pandas.core.frame import DataFrame
from requests.exceptions import HTTPError
from std_msgs.msg import String
from google.cloud.firestore import Client
from google.oauth2.credentials import Credentials


class DynamicoListener():
    """
    - iReCHeck class to listen to the dynamico firebase and publish the changes in the ROS node
    - Give the name of the collection you want to listen in the "listening_collection" in the class constructor
    - NOTE-> Google's server time is different from Switzerland timezone
    
    """

    def __init__(self, listening_collection):
        # initialize ROS node
        rospy.init_node('dynamicolistener', anonymous=True)
        # initialize publishers/subscribers
        # rospy.Subscriber([topic_name],[topic_type],[callback_function_name])
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])
        self.pubMsg = rospy.Publisher('dynamicomsg', String, queue_size=10)
        
        # get credentials information from the file
        with open('/home/bruno/catkin_ws/src/irecheck/dynamico/scripts/DYNAMICO_CREDENTIALS.TXT') as f:
            data = json.load(f)
        self.email = data['EMAIL']
        self.password = data['PASSWORD']
        self.API_KEY = data['API_KEY']
        self.user_id = data['USER_ID']   
        self.project_id = data['PROJECT_ID']

        # sign in on the Dynamico Firestore as done in https://gist.github.com/Bob-Thomas/4d9370c6b5432fb5150d3618e0ae71ba
        self.FIREBASE_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"
        response = self.sign_in_with_email_and_password(self.FIREBASE_REST_API, self.API_KEY, self.email, self.password)
        
        # use google.oauth2.credentials and the response object to create the correct user credentials
        creds = Credentials(response['idToken'], response['refreshToken'])
        self.db = Client(self.project_id, creds)

        # create an event to be notified of changes in the Dynamico Firestore
        self.dynamicoCallback = threading.Event()
    
        # watch the changes in the listening_collection only with regards to our user
        doc_ref = self.db.collection(listening_collection).where(u'userId', u'==', self.user_id)
        self.doc_watch = doc_ref.on_snapshot(self.on_snapshot)

        # keep python from exiting until this node is stopped
        rospy.spin()


    # we use the sign_in_with_email_and_password function from https://gist.github.com/Bob-Thomas/49fcd13bbd890ba9031cc76be46ce446
    def sign_in_with_email_and_password(self, url, api_key, email, password):
        request_url = "%s:signInWithPassword?key=%s" % (url, api_key)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        resp = requests.post(request_url, headers=headers, data=data)
        # check for errors
        try:
            resp.raise_for_status()
        except HTTPError as e:
            raise HTTPError(e, resp.text)
            
        return resp.json()
    

    # create a callback on_snapshot function to capture changes in the Dynamico Firestore
    def on_snapshot(self, doc_snapshot, changes, read_time):
        # create an empty list of dataframes to be populated with the changes in database and sent over ROS
        final = []

        for ch in changes:  
            # get the item as a dictionary
            item = ch.document._data
            
            # correct Google's stupidity of DateTime with Nanoseconds .... (why god???)
            # NOTE again -> Google's server time is different from Switzerland timezone
            val1 = item['createdAt']
            year,month,day,hour,minute,second,tzinfo = val1.year,val1.month,val1.day,val1.hour, val1.minute, val1.second, val1.tzinfo
            utc_time  = "%s-%s-%s %s:%s:%s"%(year, month, day,hour,minute,second) 
            item['createdAt']=utc_time

            #create a pandas dataframe with the current information or change in the firebase
            final.append(pd.DataFrame(item, index=[0]))

        # concatenate all the new changes in a single dataframe
        final = pd.concat(final, ignore_index=True)
        final = final.sort_values('createdAt', ignore_index=True)

        # convert the dataframe in a json string and publish it as a ROS message
        msg = final.to_json(orient='records')
        rospy.loginfo(msg)
        self.pubMsg.publish(msg)
        self.dynamicoCallback.set()


    # test quering the dynamico db
    def test(self):
        # diagnosesDocs = self.db.collection(u'diagnoses').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").stream()
        # diagnosesDocs = self.db.collection(u'diagnoses').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").stream()
        diagnosesDocs = self.db.collection('scores').where(u'userId', u'==', self.user_id)
        
        # convert the retrieved docs in dictionaries and extract the handwriting scores values
        for doc in diagnosesDocs.stream():
            tempDict = doc.to_dict()
            print(tempDict)
            print("\n")



#########################################################################
if __name__ == "__main__":
    try:
        # myDynamicoListener = DynamicoListener('writingDiagnoses')
        # myDynamicoListener = DynamicoListener('scores')
        myDynamicoListener = DynamicoListener('scores')
    except rospy.ROSInterruptException:
        pass
    finally:
        myDynamicoListener.doc_watch.unsubscribe()