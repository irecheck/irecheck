# System Requirements (package specific)

* mySQL Server (temporary)
* (PySide2)

# Preliminary Operations

## Install mySQL
In a terminal tab:
```
$ sudo apt update
$ sudo apt install mysql-server
```

## Install mysql-connector-python
Install pip (to check if you already have it, type `pip --version`):
```
$ sudo apt install python-pip
```
Then:
```
$ pip install mysql-connector-python
```
If the above command gives you an error (too low version of pip), upgrade pip:
```
$ pip install --upgrade pip
```
and then issue the command again. If you get a warning (wrapper too old), just restart the computer and it should disappear.

## Create the temporary fakeDynamico database and set access rules
Launch the mySQL service from terminal (insert password when prompted):
```
$ sudo mysql -u root -p
```

You will see the following output on the terminal:
```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.30-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

FakeDynamico uses a local SQL database to store its data. Create it with:
```
mysql> CREATE DATABASE fakedynamico;
```

Grant to user *dynamico* all rights on the database *fakedynamico*:
```
mysql> GRANT ALL PRIVILEGES ON fakedynamico.* TO 'dynamico'@'localhost' IDENTIFIED BY 'dynamicopw';
```

Exit the mySQL console:
```
mysql> exit
```

## Set up the irecheck package
The **irecheck** package keeps all data collected at run-time in a Pandas dataframe, which is exported to a .csv file at the end of the session.

As specified in the script *irecheckWorld.py*, the .csv file is saved inside the **~/Documents/iReCHeCk_logs/** folder.

Create the folder before running the package, or change the path.

# Package overview (TO BE UPDATED)
The **irecheck** ROS package includes the following nodes:
* **coreEngine** - master controller: it receives the record updates, the Autonomous Mode commands and the Wizard commands (when available) and appropriately dispatches commands for the robot
* **wozInterface** - it receives the record updates, displays them to the Wizard and publishes Wizard commands for the coreEngine
* **autonomousMode** - it receives the record updates, processed them and publishes Autonomous Mode commands for the coreEngine
* **qtController** - gets commands from the coreEngine and publishes commands for the QTrobot

In the final scenario, records will be written into the **myirecheck** database by the Dynamico application, as the child interacts with it.
For easy development and debugging, the script **fakeDynamico** emulates the Dynamico app and allows to add records onto the **myirecheck** database.

# Usage Guide (TO BE UPDATED)

Open a terminal tab, browse to its folder and launch the **fakeDynamico** script:
```
$ python fakeDynamico.py
```

Use the displayed commands to act upon the database.

To launch all the nodes in the iReCHeCk architecture at once, you can use the *irecheck.launch* launchfile.
The launchfile accepts an argument in input to specify whether it should launch the interface for the wizard (default), or the debug interface.

To launch the default wizard interface, **in a new terminal tab**:
```
$ roslaunch irecheck irecheck.launch debug:="0"
```

To launch the debug interface, **in a new terminal tab**:
```
$ roslaunch irecheck irecheck.launch debug:="1"
```

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

Then, for each node to launch (e.g., **dbListener**), **in a new terminal tab**:
```
$ rosrun irecheck dbListener.py
```

# Tips & Tricks

1. When you delete the table you need to rerun the code