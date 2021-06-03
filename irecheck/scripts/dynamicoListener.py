#!/usr/bin/env python

from pandas.core.frame import DataFrame
import rospy
import json
import requests
import threading
import pandas as pd

from requests.exceptions import HTTPError
from std_msgs.msg import String
from google.cloud.firestore import Client
from google.oauth2.credentials import Credentials


class DynamicoListener():
    """
    - iReCHeck class to listening the dynamico firebase and publish the changes in the ROS node
    - Give the name of the collection you want to listen in the "listening_collection" in the class constructor
    - NOTE-> Google's server time is different from Switzerland timezone
    
    """

    def __init__(self, listening_collection):
        
        self.FIREBASE_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"   # Access credentials for the Dynamico Firestore: REST endpoint

        # Getting credentials information from the file
        with open('/home/carnieto/iReCHeck/dynamico/scripts/DYNAMICO_CREDENTIALS.txt') as f:
            data = json.load(f)

        self.email = data['EMAIL']                                     # Access credentials for the Dynamico Firestore: email
        self.password = data['PASSWORD']                                                      # Access credentials for the Dynamico Firestore: password
        self.API_KEY = data['API_KEY']                        # Access credentials for the Dynamico Firestore: API_KEY
        self.user_id = data['USER_ID']   
        self.project_id = data['PROJECT_ID']

        # initialize ROS node
        self.pubMsg = rospy.Publisher('dynamicomsg', String, queue_size=10)
        rospy.init_node('dynamicolistener', anonymous=True)
        self.rate = rospy.Rate(10)
        
        # Transmited dataframe -> Not used
        self.msg_df = pd.DataFrame()

        # initialize publishers/subscribers
        # rospy.Subscriber([topic_name],[topic_type],[callback_function_name])
        # rospy.Publisher([topic_name],[topic_type],[max_queue_size])

        # sign in on the Dynamico Firestore as done in https://gist.github.com/Bob-Thomas/4d9370c6b5432fb5150d3618e0ae71ba
        response = self.sign_in_with_email_and_password(self.FIREBASE_REST_API, self.API_KEY, self.email, self.password)
        
        # use google.oauth2.credentials and the response object to create the correct user credentials
        creds = Credentials(response['idToken'], response['refreshToken'])
        self.db = Client(self.project_id, creds)

        # create an event to be notified of changes in the Dynamico Firestore
        self.dynamicoCallback = threading.Event()

        # watch the Dynamico Firestore collection (diagnoses document)
        # doc_ref = self.db.collection(u'diagnoses').where(u'userId', u'==', data["USER_ID"]).
        # doc_ref = self.db.collection(u'scores').where(u'userId', u'==', data['USER_ID']).where(u'childId', u'==', u"75DA34CC-64C4-40C5-8639-6653FBF26FDA")
        
        # watch the changes in the listening_collection only with regards to our user
        doc_ref = self.db.collection(listening_collection).where(u'userId', u'==', self.user_id) #.where(u'childId', u'==', u"75DA34CC-64C4-40C5-8639-6653FBF26FDA")

        self.doc_watch = doc_ref.on_snapshot(self.on_snapshot)


    # we use the sign_in_with_email_and_password function from https://gist.github.com/Bob-Thomas/49fcd13bbd890ba9031cc76be46ce446
    def sign_in_with_email_and_password(self, url, api_key, email, password):
        request_url = "%s:signInWithPassword?key=%s" % (url, api_key)
        headers = ***REMOVED***"content-type": "application/json; charset=UTF-8"***REMOVED***
        data = json.dumps(***REMOVED***"email": email, "password": password, "returnSecureToken": True***REMOVED***)
        
        resp = requests.post(request_url, headers=headers, data=data)
        # check for errors
        try:
            resp.raise_for_status()
        except HTTPError as e:
            raise HTTPError(e, resp.text)
            
        return resp.json()
    

    # create a callback on_snapshot function to capture changes in the Dynamico Firestore
    def on_snapshot(self, doc_snapshot, changes, read_time):
        
        print("inside snapshot")
       
        # Empty list of dataframes to be populated with the changes in database and send through ROS node afterwards
        final = []

        for ch in changes:
            # msg = ("Change-> ***REMOVED******REMOVED***".format(ch.document._data))
            # msg = ("***REMOVED******REMOVED***".format(ch.document._data))
            # rospy.loginfo(ch.document._data)
            
            # get the item as a dictionary
            item = ch.document._data
            
            # Correcting Google's stupidity of DateTime with Nanoseconds .... (why god???)
            # NOTE again -> Google's server time is different from Switzerland timezone
            val1 = item['createdAt']
            year,month,day,hour,minute,second,tzinfo = val1.year,val1.month,val1.day,val1.hour, val1.minute, val1.second, val1.tzinfo
            utc_time  = "%s-%s-%s %s:%s:%s"%(year, month, day,hour,minute,second) 
            item['createdAt']=utc_time

            #create a pandas dataframe with the current information or change in the firebase
            final.append(pd.DataFrame(item, index=[0]))


        # Concatenate all the informations received in an only dataframe
        final = pd.concat(final, ignore_index=True)
        
        final = final.sort_values('createdAt', ignore_index=True)

        # final['createdAt'] = pd.to_datetime(final['createdAt'])

        # Convert the dataframe in a json string
        msg = final.to_json(orient='records')
        
        # Publish the string by the ROS node
        self.pubMsg.publish(msg)
        rospy.loginfo("Message sent:"+ str(msg))
        self.dynamicoCallback.set()


    # test quering the dynamico db
    def test(self):
        # diagnosesDocs = self.db.collection(u'diagnoses').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").stream()
        # diagnosesDocs = self.db.collection(u'diagnoses').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").stream()
        diagnosesDocs = self.db.collection('scores').where(u'userId', u'==', self.user_id) #.where(u'childId', u'==', u"75DA34CC-64C4-40C5-8639-6653FBF26FDA")
        
        # print(type(diagnosesDocs))
        
        # convert the retrieved docs in dictionaries and extract the handwriting scores values
        for doc in diagnosesDocs.stream():
            tempDict = doc.to_dict()
            
            # scores = [-1, -1, -1, -1, -1]
            # scores[0] = tempDict[u'kinematicScore']
            # scores[1] = tempDict[u'pressureScore']
            # scores[2] = tempDict[u'staticScore']
            # scores[3] = tempDict[u'tiltScore']
            # scores[4] = tempDict[u'totalScore']
            print(tempDict)
            print("\n")



#########################################################################
if __name__ == "__main__":
    
    # myDynamicoListener = DynamicoListener('scores')
    
    
    try:
        # myDynamicoListener = DynamicoListener('writingDiagnoses')
        myDynamicoListener = DynamicoListener('scores')
        print("Class Created")
        # myDynamicoListener.test()
        rospy.spin()

    except rospy.ROSInterruptException:
        print("Exception")
        pass
    finally:
        # terminate watch on a document
        myDynamicoListener.doc_watch.unsubscribe()
        print("Done!")




##### FROM HERE ONWARDS IT'S DIRTY CODE #####

# #diagnosess = db.collection(u'analysisExercises').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").get()
# diagnosesDocs = db.collection(u'diagnoses').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").get()
# #diagnosesDocs = db.collection(u'children').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").get()

# # # [DEBUG ONLY]
# # for doc in diagnosesDocs:
# #     print("doc id: ***REMOVED******REMOVED***".format(doc.id))
# #     print("doc: ***REMOVED******REMOVED***".format(doc.to_dict()))
# #     print("\n")

# # convert the retrieved docs in dictionaries and extract the handwriting scores values
# for doc in diagnosesDocs:
#     tempDict = doc.to_dict()
#     scores = [-1, -1, -1, -1, -1]
    
#     scores[0] = tempDict[u'kinematicScore']
#     scores[1] = tempDict[u'pressureScore']
#     scores[2] = tempDict[u'staticScore']
#     scores[3] = tempDict[u'tiltScore']
#     scores[4] = tempDict[u'totalScore']
#     print(scores)
#     print("\n")


# #     print(doc.to_dict().keys())
# #     print("\n"


# #     #print(doc.to_dict())
# #     #print(f'***REMOVED***doc.id***REMOVED*** => ***REMOVED***doc.to_dict()***REMOVED***')

# # #print(element)