#!/usr/bin/env python
# * Running on http://127.0.0.1:5000/

from flask import Flask, jsonify, render_template, request, redirect, session
import sys
import copy
import rospy
# from control_publisher import RobotBehaviour
from threading import Thread
from std_msgs.msg import String
import pandas as pd
from my_utils import HistoryUtil
from comportement_control.msg import GestureCommand
sys.path.append(r'/home/jennie/irecheck/iReCheck/QT_ws/src/irecheck/platforms/script')  
#from control_publisher import RobotBehavior
from qtrobot import RobotBehavior
from qt_robot_interface.srv import *


'''
dynamico_dict = {
    'id': [1, 2],
    'fname': ["Julian", "Julian"],
    'lname': ["Blackwell", "Blackwell"],
    'language': ["en-GB", "en-GB"],
    'gender': ["m", "m"],
    'age': ["21", "21"],
    'left_right': ["r", "r"],
    'country': ["Switzerland", "Switzerland"],
    'city': ["Kilchberg", "Kilchberg"],
    'activity': ["TILT", "TILT"],
    'globalS': [1, 0],
    'staticS': [1, 0],
    'pressureS': [1, 0],
    'tiltS': [1, 0],
    'kinematicS': [1, 0],
    'level': [5, 1],
    'duration': [20, 50],
    'result': ["w", "f"]
}

df = pd.DataFrame(dynamico_dict, columns=['id', 'fname', 'lname','language', 'gender', 'age', 'left_right', 'country', 'city', 'activity', 'globalS', 'staticS', 'pressureS', 'tiltS', 'kinematicS', 'level', 'duration', 'result'])
df.set_index('id')
df.to_csv('history.csv', index=False)
print(pd.read_csv('history.csv', usecols=['fname', 'lname']))
'''

#Global variables
dynamicData = {
    'newDynamico': False,
    'coreAval': False,
    'qtAval': False,
    'newRobot': "<p>Test</p>"
}

hU = HistoryUtil()

Thread(target=lambda:rospy.init_node("flask_interface",anonymous=True,disable_signals=True)).start()

# Publishers
pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
langPub = rospy.Publisher('/robot/language', String, queue_size=10)
simPub = rospy.Publisher('/robot/simulate', String, queue_size=10)
statePub = rospy.Publisher('/robot/state', String, queue_size=10)

# service
language_config = rospy.ServiceProxy('/qt_robot/speech/config', speech_config)
res_language = language_config("fr-FR",0,0)

# Subscribers & callback functions

def newDynamicoCallback(data):
    global dynamicData
    dynamicData['newDynamico'] = True

    hU.addRow(data)

rospy.Subscriber('dynamicomsg', String, newDynamicoCallback)

def debugSubCallback(data):
    global dynamicData
    dynamicData['newRobot'] += "<p>" + data.data + "</p>"

rospy.Subscriber('robot/debug', String, debugSubCallback)


app = Flask(__name__)
app.secret_key = "woz" 

# session = { 'user_name': "Julian", 'user_surname': "Blackwell"}


@app.route('/')
def index(name=None):
    return redirect('/login');

@app.route('/login', methods=['GET', 'POST'])
def login(name=None,):
    if request.method=='POST':
        if (not len( request.form.get('fname') ) or not len( request.form.get('lname') ) ):
            print("error");
            return render_template('login.html', name=name)
        else:
            print(request.form);
            session['user_name'] = request.form.get('fname');
            session['user_surname'] = request.form.get('lname');
            return render_template('scenarios.html', name=name)
		
		
    return render_template('login.html', name=name)

	
@app.route('/reactions')
def reactions(name=None):
    if not session.get('user_name') or not len(session.get('user_name')) or not len( session.get('user_surname') ) :
        return redirect('/');

    return render_template('reactions.html', name=name)

@app.route('/scenarios')
def scenarios(name=None):
    if not session.get('user_name') or not len(session.get('user_name')) or not len( session.get('user_surname') ) :
        return redirect('/');

    return render_template('scenarios.html', name=name)

	
# woz_command can send ros messages and call ros services
@app.route("/woz",methods=['POST'])
def ros_ini():
   # say = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
    emo = rospy.Publisher('/qt_robot/emotion/show',String, queue_size=10)
   # gesture = rospy.Publisher('comportement/gesture_name',GestureCommand,queue_size=10)
   # rospy.sleep(1)
    woz_command(pub,emo)
    return("")
def woz_command(pub,emo):
    payload = request.get_json() 
    prenom = session.get('user_name')
    behaviour = RobotBehavior()
    behaviour.load_info(payload['command'],prenom)
    behaviour.realisation(pub,emo)
    return ("nothing")


@app.route('/debug', methods=['GET', 'POST'])
def debug_page():
    if not session.get('user_name') or not len(session.get('user_name')) or not len( session.get('user_surname') ) :
        return redirect('/');

    global dynamicData
    dynamicData['newDynamico'] = True

    return render_template('debug.html')

@app.route('/debug/dynamic')
def dynamic_update():
    global dynamicData

    # New data added to the database?
    nD = dynamicData['newDynamico']
    dynamicData['newDynamico'] = False

    # Update roscore status
    try:
        rospy.get_master().getPid()
        # print("Roscore running")
        dynamicData['coreAval'] = True
    except:
        # print("Roscore not running")
        dynamicData['coreAval'] = False
    cA = dynamicData['coreAval']

    # Update QTRobot status
    if dynamicData['coreAval']:
        topics = rospy.get_published_topics()
        # print(['/rosout', 'rosgraph_msgs/Log'] in topics)
        if ['/qt_robot/head_position/command', 'TODO'] in topics:
            dynamicData['qtAval'] = True
        else:
            dynamicData['qtAval'] = False
    qA = dynamicData['qtAval']

    # Get last 10 entries in the DB
    ten = ""
    if nD:
        ten = pd.read_csv('history.csv', index_col='id').tail(10).to_html()

    # Load debug messages from Robot
    nR = dynamicData['newRobot']
    dynamicData['newRobot'] = ""
    
    return jsonify(newDynamico=nD, coreAval=cA, qtAval=qA, latestHistory=ten, newRobot=nR)

@app.route('/history')
def history_page():
    if not session.get('user_name') or not len(session.get('user_name')) or not len( session.get('user_surname') ) :
        return redirect('/')

    hU.changeUser(session.get('user_surname'))

    userInfo = hU.getUserInfo()
    session['user_age'] = userInfo['user_age']
    session['user_gender'] = userInfo['user_gender']
    session['user_dext'] = userInfo['user_dext']

    return render_template('history.html')

@app.route('/history/raw')
def raw_user_data():
    return hU.getUserTableHTML()

@app.route('/history/dynamic', methods=['GET'])
def history_dynamic():
    # csv = pd.read_csv('history.csv', index_col='id')
    # csv.to_html()
    return jsonify(hU.getUserData())

@app.route('/ros', methods=['GET', 'POST'])
def receive():
    if request.method == 'POST':
        print(request.form)
        cmd = request.form.get('rosMessage')
        if cmd == "PUBLISH":
            rospy.loginfo("Published to QT")
            pub.publish("Test")
            return "Published data to QT"
        elif cmd == "TEST":
            return "Tested"
        elif cmd == "MESSAGE":
            return request.form.get('rosMessage')
        elif cmd == "QTSAY":
            pub.publish(request.form.get('data'))
            rospy.loginfo("Published to QT speech")
            return "Made QT say something!"
        elif cmd == "LANGUAGE":
            langPub.publish(request.form.get('data'));
            return "Language changed"
        elif cmd == "SIM":
            simPub.publish(request.form.get('data'));
        elif cmd == "STATE":
            statePub.publish(request.form.get('data'));
        else:
            print("Unrecognized message: " + cmd)
            return "Unrecognized message: " + cmd

    return redirect('/debug')

@app.route('/util', methods=['GET'])
def random_util():
    # csv = pd.read_csv('history.csv', header=False)
    # return csv.to_html()
    return hU.getUserTableHTML()
	
if __name__ == "__main__":
    # Does not work with debug mode on True due to possible incompatibility with ROS Subscriber
    app.run(host= '0.0.0.0',debug=True)
