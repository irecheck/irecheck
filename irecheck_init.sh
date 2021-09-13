#! /bin/sh.

rosrun dynamico dynamico
rosrun qt_behaviour_control qtrobot_auto.py Student Therapist
rosrun irecheck decisionMaker.py
rosrun irecheck irecheckManager.py 