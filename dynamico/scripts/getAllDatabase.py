#!/usr/bin/env python3

# import rospkg as rospy
import rospy
import json
import requests
import threading
import os
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
    - NOTE-> Google's server time is different from Swiss timezone
    
    """

    def __init__(self, listening_collection_1):#, listening_collection_2):
        
        # initialize ROS node
        rospy.init_node('dynamicolistener', anonymous=True)
       
        # initialize publishers/subscribers
        self.pubMsg = rospy.Publisher('dynamicomsg', String, queue_size=10)
        
        # get credentials information from the file
        path = os.path.realpath(__file__).replace('getAllDatabase.py','')
        with open(path + '/DYNAMICO_CREDENTIALS_PARIS.txt') as f:
            data = json.load(f)

        print ("DATA> \n", data)
        print(f"Initialing listener to collection: <<{listening_collection_1}>>")

        self.email = data['EMAIL']
        self.password = data['PASSWORD']
        self.API_KEY = data['API_KEY']
        self.user_id = data['USER_ID']   
        self.project_id = data['PROJECT_ID']

        # sign in on the Dynamico Firestore as done in https://gist.github.com/Bob-Thomas/4d9370c6b5432fb5150d3618e0ae71ba
        self.FIREBASE_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"
        response = self.sign_in_with_email_and_password(self.FIREBASE_REST_API, self.API_KEY, self.email, self.password)
        
        self.listening_collection = listening_collection_1

        # use google.oauth2.credentials and the response object to create the correct user credentials
        creds = Credentials(response['idToken'], response['refreshToken'])
        self.db = Client(self.project_id, creds)

        # create an event to be notified of changes in the Dynamico Firestore
        self.dynamicoCallback = threading.Event()
    
        # watch the changes in the listening_collection only with regards to our user
        doc_ref = self.db.collection(listening_collection_1).where(u'userId', u'==', self.user_id)
        self.doc_watch = doc_ref.on_snapshot(self.on_snapshot)

        # self.doc_watch.on_snapshot()

        # [DEBUG ONLY]
        print("Waiting for messages")

        # # keep python from exiting until this node is stopped
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
            # [DEBUG ONLY]
            # print(resp)
        except HTTPError as e:
            raise HTTPError(e, resp.text)
            
        return resp.json()
    


    # Callback for firebase listener

    def on_snapshot(self, doc_snapshot, changes, read_time):
        
        #print("LEN   " + self.listening_collection + " : ", len(changes)) 

        final_csv = pd.DataFrame()

        # Getting every entry of the 
        for current_entry in changes:

            item = current_entry.document._data
            name = current_entry.document.id
   
            # Correcting nested dict of writing diagnoses
            try:
                mid_dict = item['features']
                item.update(mid_dict)
                del item['features']
                # print ("ITEM->", item ) 

            except:
                # print("It is not a writing analysis.")
                pass
           
         
            if self.listening_collection == 'scores':
                item['type'] =  'activity'
            elif self.listening_collection == 'writingDiagnoses':
                item['type'] =  'assessment'

            # correct Google's stupidity of DateTime with Nanoseconds .... (why god???)
            # NOTE again -> Google's server time is different from Switzerland timezone
            val1 = item['createdAt']
            year,month,day,hour,minute,second,tzinfo = val1.year,val1.month,val1.day,val1.hour, val1.minute, val1.second, val1.tzinfo
            utc_time  = "%s-%s-%s %s:%s:%s"%(year, month, day,hour,minute,second) 
            item['createdAt']=utc_time
            temp_df = pd.DataFrame(item, index=[0])
            final_csv = pd.concat([final_csv,temp_df])
            print(final_csv)

        # HERE is where it saves the file to CSV
        csv_name = "CSV_NAME_HERE"+".csv"
        final_csv.to_csv(csv_name)
        print("FILE SAVED IN " + os.getcwd() + '/' + csv_name)

           
            
        # else:
        #     # [DEBUG ONLY]
        #     print("\n\n-------------- Fisrt time. No message was sent --------------\n")

   


#########################################################################
if __name__ == "__main__":
    
  
    try:
        myDynamicoListener = DynamicoListener('writingDiagnoses')
        myDynamicoListener_2 = DynamicoListener('scores')

    
        print("My code never gets here!")

    except rospy.ROSInterruptException:
        pass

    finally:
        myDynamicoListener.doc_watch.unsubscribe()
        myDynamicoListener_2.doc_watch.unsubscribe()
        print("Done!")
