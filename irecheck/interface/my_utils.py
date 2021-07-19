import pandas as pd

class HistoryUtil:
    def __init__(self):
        print("Created instance of HistoryUtil")
        self.lastName = '???'
<<<<<<< HEAD
        self.info = {'user_age': '???', 'user_gender': '???', 'user_dext': '???'}
=======
        self.info = ***REMOVED***'user_age': '???', 'user_gender': '???', 'user_dext': '???'***REMOVED***
>>>>>>> 8832a7b795d6e3fb29254763f5a2a25dadd29e4b
        self.shouldUpdate = True
        self.size = 0
        self.levels = [0, 0, 0, 0, 0]
        self.activity = [0, 0, 0, 0]
        self.nSuccess = 0
        # self.htmlTable = ""

    def addRow(self, data):
        # Append new row to CSV file
        d = data.data.split(" ")
        newRow = pd.DataFrame(data=[d])
        newRow.to_csv('history.csv', mode='a', header=False, index=False) # Append mode

        # Update data if new row is relevant to current user
        # Note: 2nd column = last name, 15th col = level number, 17th col = win/fail
        if d[2] == self.lastName:

            # Update user info if no data previously available
            if (self.size == 0):
                self.info['user_age'] = d[5]
                self.info['user_gender'] = d[4]
                self.info['user_dext'] = d[6]

            self.shouldUpdate = True;
            self.size += 1
            self.levels[d[15] - 1] += 1
            updateActivity(d[9]);
            if d[17] == 'w':
                self.nSuccess += 1

    # Note: Use dictionary (better) to store activity numbers TODO
    def updateActivity(self, act):
        if act == "STATIC":
            self.activity[0] += 1
        elif act == "TILT":
            self.activity[1] += 1
        elif act == "PRESSURE":
            self.activity[2] += 1
        elif act == "KINEMATIC":
            self.activity[3] += 1
        else:
            print("Test or unknown activity: " + act)       
    
    def changeUser(self, newUser):
        if self.lastName == newUser:
            print("User unchanged: " + newUser)
            self.shouldUpdate = True
        else:
            # Change to data relevant to newUser
            print("Switched to new user: " + newUser)
            self.lastName = newUser

            # Get new dataframe relevant to user
            df = pd.read_csv('history.csv', index_col='id')
            user_df = df[df.lname.eq(newUser)]

            # self.htmlTable = user_df.to_html(table_id="rawUserData")

            # Update number of entries
            self.size = len(user_df.index)

            # Update user info if possible
<<<<<<< HEAD
            self.info = {'user_age': '???', 'user_gender': '???', 'user_dext': '???'}
=======
            self.info = ***REMOVED***'user_age': '???', 'user_gender': '???', 'user_dext': '???'***REMOVED***
>>>>>>> 8832a7b795d6e3fb29254763f5a2a25dadd29e4b
            if (self.size > 0):
                row = user_df.iloc[0]
                self.info['user_age'] = row['age']
                self.info['user_gender'] = row['gender']
                self.info['user_dext'] = row['left_right']

            # Reset values before counting again
            self.resetValues()
            # Recount number of times a level was played
            for i in user_df['level']:
                self.levels[i - 1] += 1
            # Recount number of successes
            for wF in user_df['result']=='w':
                if wF:
                    self.nSuccess += 1
            # Recount number of times an activity was played
            for act in user_df['activity']:
                self.updateActivity(act)

            # Note: TODO can merge into one iteration

    def resetValues(self):
        self.levels = [0, 0, 0, 0, 0]
        self.activity = [0, 0, 0, 0]
        self.nSuccess = 0
        self.shouldUpdate = True

    def getUserTableHTML(self):
        df = pd.read_csv('history.csv', index_col='id')
        user_df = df[df.lname.eq(self.lastName)]
        return user_df.to_html()

    def getUserData(self):
<<<<<<< HEAD
        toSend = {
=======
        toSend = ***REMOVED***
>>>>>>> 8832a7b795d6e3fb29254763f5a2a25dadd29e4b
            'shouldUpdate': self.shouldUpdate,
            'size': self.size,
            'levels': self.levels,
            'nSuccess': self.nSuccess,
            'activity': self.activity #,
            # 'historyTable': self.getUserTableHTML()
<<<<<<< HEAD
        }
=======
        ***REMOVED***
>>>>>>> 8832a7b795d6e3fb29254763f5a2a25dadd29e4b
        self.shouldUpdate = False
        return toSend

    def getUserInfo(self):
        return self.info
        
