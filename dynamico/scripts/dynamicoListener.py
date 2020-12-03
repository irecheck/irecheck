#!/usr/bin/env python

import json
import requests
from requests.exceptions import HTTPError
from google.cloud.firestore import Client
from google.oauth2.credentials import Credentials

#  variables
FIREBASE_REST_API = "https://identitytoolkit.googleapis.com/v1/accounts"

email = "email address" 
password = "password"
API_KEY = "api-key sample"

# Use the google verify password REST api to authenticate and generate user tokens
def sign_in_with_email_and_password(api_key, email, password):
    request_url = "%s:signInWithPassword?key=%s" % (FIREBASE_REST_API, api_key)
    headers = ***REMOVED***"content-type": "application/json; charset=UTF-8"***REMOVED***
    data = json.dumps(***REMOVED***"email": email, "password": password, "returnSecureToken": True***REMOVED***)
    
    resp = requests.post(request_url, headers=headers, data=data)
    # Check for errors
    try:
        resp.raise_for_status()
    except HTTPError as e:
        raise HTTPError(e, resp.text)
        
    return resp.json()


# We use the sign_in_with_email_and_password function from https://gist.github.com/Bob-Thomas/49fcd13bbd890ba9031cc76be46ce446
response = sign_in_with_email_and_password(API_KEY, email, password)
# Use google.oauth2.credentials and the response object to create the correct user credentials
creds = Credentials(response['idToken'], response['refreshToken'])

# using the credentials build in https://gist.github.com/Bob-Thomas/4d9370c6b5432fb5150d3618e0ae71ba
db = Client("dynamico-dev", creds)

#diagnosess = db.collection(u'analysisExercises').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").get()
#diagnosess = db.collection(u'diagnoses').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").get()
diagnosess = db.collection(u'children').where(u'userId', u'==', u"TXGCcUC6u5duIO6VRhfnYAXXwTg2").get()

for doc in diagnosess:
    print("doc id: ***REMOVED******REMOVED***".format(doc.id))
    print("doc: ***REMOVED******REMOVED***".format(doc.to_dict()))
    print("\n")
    element = doc.to_dict()
    #csvData = decoder(element[u'csvData'])
    #childId = element[u'childId']


    #print(doc.to_dict())
    #print(f'***REMOVED***doc.id***REMOVED*** => ***REMOVED***doc.to_dict()***REMOVED***')


print(element)
