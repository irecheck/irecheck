# * Running on http://127.0.0.1:5000/

from flask import Flask, jsonify, render_template, request, redirect, session
import sys
import copy
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from platforms.msg import NameInfo
sys.path.append(r'/home/jennie/irecheck_ws/src/irecheck/platforms/script/Version1')  
#from control_publisher import RobotBehavior
from qtrobot import RobotBehavior
from threading import Thread

Thread(target=lambda:rospy.init_node("flask_interface",anonymous=True,disable_signals=True)).start()


app = Flask(__name__)
app.secret_key = "woz" 

#session = ***REMOVED*** user_name: ""; user_surname= ""***REMOVED***

@app.route('/')
def index(name=None):
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login(name=None):
    if request.method=='POST':
        if (not len( request.form.get('fname') ) or not len( request.form.get('lname') ) ):
            print("error")
            return render_template('login.html', name=name)
        else:
            print(request.form)
            session['user_name'] = request.form.get('fname')
            session['user_surname'] = request.form.get('lname')
            session['teacher_name'] = request.form.get('fname2')
            name_info = rospy.Publisher('/woz/nameinfo',NameInfo,queue_size=10)
            name_info.publish(str(session.get('user_name')),str(session.get('user_surname')),str(session.get('teacher_name')))
            return render_template('scenarios.html', name=name)
		
		
    return render_template('login.html', name=name)

	
@app.route('/reactions')
def reactions(name=None):
    if not session.get('user_name') or not len(session.get('user_name')) or not len( session.get('user_surname') ) :
        return redirect('/')

    return render_template('reactions.html', name=name)

@app.route('/scenarios')
def scenarios(name=None):
    if not session.get('user_name') or not len(session.get('user_name')) or not len( session.get('user_surname') ) :
        return redirect('/')

    return render_template('scenarios.html', name=name)

	
# woz_command can send ros messages and call ros services
@app.route("/woz",methods=['POST'])
def ros_ini():
    say = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
    emo = rospy.Publisher('/qt_robot/emotion/show',String, queue_size=10)
    button = rospy.Publisher('/woz/button',String,queue_size=10)
    prenom = str(session.get('user_name'))
    nom = str(session.get('user_surname'))
    prenom2 = str(session.get('teacher_name'))
    woz_command(button,prenom,nom,prenom2,say,emo)
    return("")

def woz_command(button,prenom,nom,prenom2,say,emo):
    payload = request.get_json() 
    button.publish(payload['command'])
    behaviour = RobotBehavior()
    behaviour.load_info(payload['command'],prenom,nom,prenom2)
    behaviour.realisation(say,emo)
    return ("")

	
if __name__ == "__main__":
    app.run(host= '0.0.0.0',debug=True)
