# System Requirements (package specific)

* SMACH (ROS package for Finite State Machine management)

# Preliminary Operations

## Download and set up SMACH
Move into your catkin workspace (typically, inside the **catkin_ws/src/** folder) and clone the SMACH package inside it:
```
$ git clone https://github.com/ros/executive_smach.git 
```
Run catkin_make to generate SMACH messages and services:
```
$ cd ~/catkin_ws
$ catkin_make
```

## Set up the irecheck package
The **irecheck** package runs the Finite State Machine managing the robot's autonomous behaviour and keeps all data collected at run-time in a Pandas dataframe, which is exported to a .csv file at the end of the session.

The .csv file is saved inside the **~/Documents/iReCHeCk_logs/** folder.

If you haven't done it already, create the folder before running the package, or change the path.

# Package overview (TO BE UPDATED)
The **irecheck** ROS package includes the following nodes:
* **coreEngine** - master controller: it receives the record updates, the Autonomous Mode commands and the Wizard commands (when available) and appropriately dispatches commands for the robot
* **wozInterface** - it receives the record updates, displays them to the Wizard and publishes Wizard commands for the coreEngine
* **autonomousMode** - it receives the record updates, processed them and publishes Autonomous Mode commands for the coreEngine
* **qtController** - gets commands from the coreEngine and publishes commands for the QTrobot

In the final scenario, records will be written into the **myirecheck** database by the Dynamico application, as the child interacts with it.
For easy development and debugging, the script **fakeDynamico** emulates the Dynamico app and allows to add records onto the **myirecheck** database.

# Usage Guide (TO BE UPDATED)
To launch all the nodes in the iReCHeCk package at once, you can use the *irecheck.launch* launchfile.

When using a launchfile, you don't see the ROS nodes in different terminal tabs.
In this case, you might want to make sure that the topics are correctly published by the nodes, by echoing them.

**In a new terminal tab**:
```
$ rostopic list
```
will list all active topics. To echo the messages sent in one of them (e.g. */irecheck/robotcommand*):
```
$ rostopic echo /irecheck/robotcommand
```

ALTERNATIVELY, you can launch each node individually, from a new terminal tab.

In this case, **in a new terminal tab**, start with launching the *roscore*:
```
$ roscore
```

Then, for each node to launch (e.g., **irecheckWorldManager**), **in a new terminal tab**:
```
$ rosrun irecheck irecheckWorldManager.py
```

# Tips & Tricks

1. When you delete the table you need to rerun the code