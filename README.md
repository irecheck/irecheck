# System Requirements

* Ubuntu 20.04
* ROS Noetic
* Python 3.8 + Pandas (1.2.4)
* QTrobot

# Preliminary Operations

## Install ROS Noetic
Follow the instructions on http://wiki.ros.org/noetic/Installation/Ubuntu

Finalize the configuration and setup of the ROS environment following the instructions on http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment

If you are not familiar with ROS, we recommend you to go through the Beginner Level Tutorials (http://wiki.ros.org/ROS/Tutorials), up to **[16] Examining the Simple Service and Client** included.

It is very convenient to have access to the ROS commands and the catkin workspace from all terminal shells.
To do so, edit the .bashrc file to source them:
```
$ gedit .bashrc
```
And add at the end of the file the lines:
```
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
```

## Install Pandas
Make sure you have Python 3.8 installed, with `python3 --version`.

Install pip (to check if you already have it, type `pip --version`):
```
$ sudo apt install python3-pip
```
Then:
```
$ sudo -H pip3 install pandas
```

## Configure your ROS Environment for QTrobot (I HAVEN'T CHECKED THIS SECTION YET AFTER UPGRADE)
```
$ git clone https://github.com/luxai-qtrobot/software.git
```

Browse inside the cloned folder (called *software*), then copy the content of the *headers* folder into your catkin *devel* folder:
```
$ cp -r headers/* ~/catkin_ws/devel/
```

Make sure the QTrobot is plugged and on and connect your laptop to the WiFi network of the robot (for the CHILI robot, the network SSID is *QT109* and the password is written on the index page of the QTrobot User Manual).

In a terminal tab, get the IP ADDRESS of your laptop (it should be something like 10.42.0.***):
```
$ ifconfig
```

Update your *.bash_aliases* file to use the roscore of QTrobot:
```
$ gedit ~/.bash_aliases
```
And add at the end of the file the lines:
```
source /opt/ros/kinetic/setup.bash
source ~/catkin_ws/devel/setup.bash

## QTrobot
export ROS_IP=<your IP address>
export ROS_MASTER_URI=http://192.168.100.1:11311
```

**IMPORTANT** The above exports make your ROS **always** use the roscore of QTrobot. If you want to use your own roscore, comment those lines.

To check that the environment is setup correctly, in a new terminal tab list all the active ROS topics:
```
$ rostopic list
```

If you setup the system correctly, you should see all the robot's topics:
```
/add_file_to_robot
/camera/color/image_raw
/find_object/objects
/info
/interactive_interface_notes
/kid_tablet_images
/objectsStamped
/qt_robot/audio/play
/qt_robot/behavior/talkAudio
/qt_robot/behavior/talkText
/qt_robot/emotion/show
/qt_robot/gesture/play
/qt_robot/head_position/command
/qt_robot/joints/state
/qt_robot/left_arm_position/command
/qt_robot/motors/states
/qt_robot/right_arm_position/command
/qt_robot/speech/say
/robAPL_input_events
/robAPL_input_game
/robot_add_file_request
/robot_add_file_response
/rosout
/rosout_agg
/tf
```
and you can call them directly from terminal, e.g.:
```
$ rostopic pub /qt_robot/speech/say std_msgs/String "data: 'Success'"
```

If you have problems in sending command to QTrobot (and you did all the above steps correctly), try disabling your firewall:
```
$ sudo ufw disable
```

## Connecting your PC to both QTrobot AND Internet (Using WiFi dongle)

### Installing and setting up the USB dongle (ONLY FIRST TIME)
With kernel 5.4 (check with “uname -a”), the following worked on Ubuntu 20.04 (with a few restarts) - testing on 18.04:
```
$ git clone https://github.com/aircrack-ng/rtl8814au.git
$ cd rtl8814au
$ sudo make dkms_install
```
### Configuring networks (Everytime)
1. Connect USB WiFi to “QT109” and PC WiFi to Internet Network Wifi 
```
$ ifc     					# verify connections
```

2. Configure the routing table
```
$ sudo ip route flush cache
$ sudo ip route flush table main
$ sudo route add -net 10.42.0.0/24 <<wlxd03745b39aa4>>                    # QTRP/ROS through USB WiFi (“ifconfig”)
$ sudo ip route add 192.168.100.1 via 10.42.0.1 dev <<wlxd03745b39aa4>>   # fix for services
$ sudo route add -net 0.0.0.0/0 wlp59s0                                   # rest through the PC WiFi (“ifconfig”)*
$ sudo route -n                                                           # Verify the routing table
```

With the dongle, the ROS master IP will also change, so make sure that you have the following confgurations on the ROS IPs:
```
export ROS_IP=10.42.0.208                    # local IP from the **dongle** took in ifconfig 
export ROS_MASTER_URI=http://10.42.0.1:11311 # Note the 10.42.0.1 instead of 192.168.100.1

```

3. Check whether it worked by sending commands to the robot
```
$ rostopic pub -1 /qt_robot/speech/say std_msgs/String "data: 'Hi'"
$ rosservice call /qt_robot/behavior/talkText "message: 'I am QT.'" 
```

4. Voilá!

If you are sure that it worked, you can add all these lines in your bash_alias in a function to speed up the configuration process.

1. open the bash aliases file:
```
sudo gedit ~/.bash_aliases
```

2. create functions with the configurations:
```
config_rounter_table(){
sudo ip route flush table main
sudo route add -net 10.42.0.0/24 wlxd03745b4cad0	
sudo ip route add 192.168.100.1 via 10.42.0.1 dev wlxd03745b4cad0 
sudo route add -net 0.0.0.0/0 wlp0s20f3 
}


qtrobot_add_ROS_IPS(){
sed -i '$ a #QTrobot' ~/.bash_aliases
sed -i '$ a export ROS_IP=10.42.0.208' ~/.bash_aliases
sed -i '$ a export ROS_MASTER_URI=http:\/\/10.42.0.1:11311' ~/.bash_aliases
source ~/.bashrc
}

```

3. Use the function in the terminal after conecting and turning on the devices
```
config_rounter_table
```

**NOTE** You need all the same devices you used for configuring to make it work with your alias

***Important*** Do NOT forget to set the robot's ros node as the master node (export ROS_IP=... and export ROS_MASTER_URI=...)


## Set up the iReCHeCk ROS package
Clone the content of this repo inside your catkin workspace (typically, inside the **catkin_ws/src/** folder).

ROS services rely on autogenerated C++ code (yep, even if you're only programming in Python), that is created by catkin_make:
```
$ cd ~/catkin_ws
$ catkin_make
```

iReCHeCk keeps all data collected at run-time in a Pandas dataframe, which is exported to a .csv file at the end of the session.

The .csv file is saved inside the **~/Documents/iReCHeCk_logs/** folder.

Create the folder before running the package, or change the path.


## Setting the packages inside the robot

Copy the packages of the path «path_of_inseders_packages», present in this repo, inside the rotobt (head) in the path "~/catkin_ws/src" with the comand:
```
scp -r irecheck/platforms/qt_robot/«package_name»/ qtrobot@10.42.0.1:~/catkin_ws/src/
```
List of packages:
- qt_behaviour_control
- woz_interface

**TO DO:** Update commands for Woz_interface

To have these packages running, call them form inside (ssh) the robot:
```
ssh qtrobot@10.42.0.1
rosrun qt_behaviour_control qtrobot_auto.py 
```
Then, you can send commands trough ros topics to run the behaviors:
```
self.pubMsg = rospy.Publisher('/irecheck/button_name', String, queue_size=10) #Create the publisher in the topic
self.pubMsg.publish('bonjour')  #publishes the request for the 'bonjour' behavior 
```
The options of behavior are:

- identifie_sentiments = ["la_joie","amusement","la_colere", "la_motivation", "la_fatigue", "la_tristesse", "la_fierte", "etonnement"]
- interagit_avec_adulte = ["adulte_accord","demande_adulte","que_pense","monsieur","madame"]
- questionne_reflechir = ["bien","cest_mieux", "tu_mexplique","important","ensuite","pk_pas_bien","tu_es_sur","plus_simple","plus_difficile","bien_mal","pas_marche","pourquoi"]
- QT_ecrit = ["ecrit","senslettre","fermelettre","endroitlettre","bien_comme_toi"]
- commente_jeux = ["triche","facile","pas_trop_vite", "boum"]
- bugue_malade = ["tu_relances","je_bugue","fatigue","je_rouille","attends","malade"]
- QT_defend = ["et_alors","jai_progresse","cest_difficile","fais_mon_mieux","tas_gagne","ma_tablette","pas_mal","je_trouve_pas"]
- QT_encourage = ["respire","ecris_mal","cest_pas_grave","fera_mieux","courage","rate","difficile","pas_content_moi","tu_mecoute","on_essaye"]
- felicite_applaudit = ["bravo","je_suis_fort","cest_bien", "tu_es_fort","nous_sommes_fort","fier_de_toi","applique","tu_perseveres"]
- taquine_plaisante = ["aie","ahahah","muscle"]
- QT_papote = ["merci","repete","oui","non","sais_pas_toi","et_toi"]
- QT_conclue = ["dernier_jeu","cetait_bien","tu_maide","mes_progres","bisou","bcp_travaille","il_est_lheure","arrete","au_revoir"]
- gere_rythme = ["pause","change_jeu","choisis_jeu"]
- explique_scenario = ["je_mappelle_qt","tu_veux_maider","tu_maides_encore","adieu","adieu2"]
- lance_seance = ["tu_viens","ton_nom","ca_va",**"bonjour"**]
- Analyse = ["analyse_lance"]
- Helicoptere = ["tilt_lance","tilt_expli","tilt_complet"]
- Poursuite = ["poursuite_lance","poursuite_expli","poursuite_complet"]
- Sous_marin = ["pression_lance","pression_expli","pression_complet"]
- Apprenti = ["cowritter_lance","cowritter_expli_class","cowritter_complet"]


**NOTE**: All the behavior are in French!

# Usage Guide
Refer to the **README** guides of the single packages.

# Tips & Tricks (TO BE UPDATED)

Did you push something you shouldn't have and now Google, FBI, CIA and Dynamico are all after you? No worries! With git you can change the past:
1. make a new commit deleting the file(s) that shouldn't have been uploaded (e.g. the infamous DYNAMICO_CREDENTIALS.txt)
2. cd Documents (or some other random place)
3. git clone --mirror https://github.com/irecheck/irecheck.git
4. download the BFG tool from https://rtyley.github.io/bfg-repo-cleaner/ and place the .jar in the same folder containing your repo
5. run the appropriate BFG command (e.g. java -jar bfg-1.14.0.jar --delete-files DYNAMICO_CREDENTIALS.txt irecheck.git)
6. cd irecheck.git
7. git reflog expire --expire=now --all && git gc --prune=now --aggressive
8. git push
9. to check if it really worked, go to the unlucky commit and browse the repo at that point: the file(s) should no longer appear!

Some other useful tips:
1. To make a python script executable (e.g. "scripts/dbListener.py"): 
```
$ chmod +x scripts/dbListener.py
```

2. Whenever you create a new ROS message or ROS service in your package, you need to update CMakeLists.txt (and possibly package.xml as well) accordingly, and then re-run catkin_make. Refer to the ROS Tutorial http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv for instructions on how to do so.

3. If you want to slow down the movement of the QT to make idle movement more natural run the following commands:

rosservice call /qt_robot/motors/setVecity "parts:
- 'left_arm'
velocity: 4"

rosservice call /qt_robot/motors/setVecity "parts:
- 'right_arm'
velocity: 4"

4. To clone7pull/push from or to a branch, the syntax for the git command is:
```
$ git clone -b dorsa ssh://git@c4science.ch/source/iReCHeCk_repo.git
```

5. If you get the error ``unable to locate package python-pip`` when installing pip, try:
```
$ sudo add-apt-repository universe 
$ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip2.py
$ sudo python get-pip2.py
```
