# System Requirements (package specific)

* Requests Python library
* Firestore Python library

# Preliminary Operations

## Install the Requests library
In a terminal tab:
```
$ python3 -m pip install requests
```

## Install the Firestore library
In a terminal tab:
```
$ pip install --upgrade google-cloud-firestore
```

## Configure your system to access the Dynamico Firestore database
Place the **DYNAMICO_CREDENTIALS.TXT** file, that you should have received separately, in the *scripts* folder.

**Do NOT upload those information on the public repo!!**

# Package overview

# Package TODO

* fix get of collections (all the relevant ones)
* extract meaningful elements from the returned dictionaries

# Usage Guide
In a terminal tab, start with launching the *roscore* (skip this step if it is already running):
```
$ roscore
```

Then, **in a new terminal tab**:
```
$ rosrun dynamico dynamicoListener.py
```

# Tips & Tricks
