import sys
import mysql.connector
from mysql.connector import Error


# list available commands
def commandMenu():
    print("\n\nThis is the Dynamico simulator to fill the fakedynamico DB. Implemented commands are:")
    print("DEL - delete the dynamico_table from the DB")
    print("WIN - add the record of a successful game episode to the DB")
    print("FAIL - add the record of an unsuccessful game episode to the DB")
    print("TEST - add the record of a test to the DB")
    print("CST - add a completely custom record")
    print("CSTA - add a custom record about a game to the DB")
    print("CSTT - add a custom record about a test to the DB")
    print("LAST - display on terminal the most recent record in the DB")
    print("ALL - display on terminal all records in the DB")
    print("COLS - show the field names of the dynamico_table in the DB")
    print("CLEAR - clear the content of the dynamico_table in the DB")
    print("Q - quit the program")
    command = raw_input('Type the command to run: ')
    return command


# establish connection to the fakedynamico database
def connectDB():
    # connect to the fakedynamico database (assumed to be located in the same computer)
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='fakedynamico',
                                             user='dynamico',
                                             password='dynamicopw')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            # # [DEBUG] delete the table
            # # execute if the fields need to be modified
            # sql_command = "DROP TABLE IF EXISTS dynamico_table"
            # cursor.execute(sql_command) 

            # create the database if it doesn't exist (fields are TEMPORARY)
            sql_command = """CREATE TABLE IF NOT EXISTS dynamico_table ( 
                             id INT AUTO_INCREMENT PRIMARY KEY,
                             fname TEXT,
                             lname TEXT,
                             language TEXT,
                             gender TEXT, 
                             age INT NOT NULL,
                             left_right TEXT,
                             country TEXT,
                             city TEXT,
                             activity TEXT,
                             globalS REAL,
                             staticS REAL,
                             pressureS REAL,
                             tiltS REAL,
                             kinematicS REAL,
                             level INT,
                             duration REAL,
                             result TEXT);"""
            cursor.execute(sql_command)

    except Error as e:
        print("Error while connecting to MySQL", e)

    # report successful connection
    return connection, cursor


# delete the dynamico_table in the fakedynamico database
def deleteTable(cursor):
    sql_command = "DROP TABLE IF EXISTS dynamico_table"
    cursor.execute(sql_command)


# add a record to the fakedynamico database
def addRecord(connection, cursor, type):
    # add a record related to a successful episode (win)
    if type == "WIN":
        sql_command = """INSERT INTO dynamico_table
                         (fname, lname, language, gender, age, left_right, country, city, activity, level, duration, result)
                         VALUES
                         ("Dorsa", "Safaei", "en-GB", "f", 29, "r","iran", "tehran", "worm", 2, 9.8, "w");"""
        cursor.execute(sql_command)
        connection.commit()
        print(cursor.rowcount, "WIN record inserted.")
    # add a record related to an unsuccessful episode (fail)
    elif type == "FAIL":
        sql_command = """INSERT INTO dynamico_table
                         (fname, lname, language, gender, age, left_right, country, city, activity, level, duration, result)
                         VALUES
                         ("Dorsa", "Safaei", "en-GB", "f", 29, "r","iran", "tehran", "worm", 2, 9.8, "f");"""
        cursor.execute(sql_command)
        connection.commit()
        print(cursor.rowcount, "FAIL record inserted.")
    # add a custom record related to a game
    elif type == "CSTA":
        game = raw_input('Activity played (STATIC/TILT/PRESSURE/KINEMATIC): ')
        level = raw_input('Level (1, 2, 3, 4, 5): ')
        outcome = raw_input('Outcome (w/f): ')
        sql_command = """INSERT INTO dynamico_table
                     (fname, lname, language, gender, age, left_right, country, city, activity, level, duration, result)
                     VALUES("Dorsa","Safaei", "en-GB", "f", 29, "r","iran", "Tehran", "%s", %s, 9.8, "%s");""" % (game, level, outcome)
        cursor.execute(sql_command)
        connection.commit()
        print(cursor.rowcount, "CUSTOM activity record inserted.")
    # add a custom record related to a test
    elif type == "CSTT":
        globalS = raw_input('Global score (0-1): ')
        staticS = raw_input('Static score (0-1): ')
        pressureS = raw_input('Pressure score (0-1): ')
        tiltS = raw_input('Tilt score (0-1): ')
        kinematicS = raw_input('Kinematic score (0-1): ')
        sql_command = """INSERT INTO dynamico_table
                         (fname, lname, language, gender, age, left_right, country, city, activity, globalS, staticS, pressureS, tiltS, kinematicS)
                         VALUES
                         ("Dorsa", "Safaei", "en-GB", "f", 29, "r","iran", "tehran", "test", %s, %s, %s, %s, %s);""" % (globalS, staticS, pressureS, tiltS, kinematicS)
        cursor.execute(sql_command)
        connection.commit()
        print(cursor.rowcount, "CUSTOM activity record inserted.")
    # add a completely custom record
    elif type == "CST":
        fname = raw_input('First name: ')
        lname = raw_input('Last name: ')
        language = raw_input('Language (e.g. "en-GB, en-US, fr-CH, fr-FR, it-IT"): ')
        gender = raw_input('Gender (f/m): ')
        age = raw_input('Age (in years): ')
        left_right = raw_input('Dexterity (l/r): ')
        country = raw_input('Country of origin: ')
        city = raw_input('City of residence: ')
        activity = raw_input('Activity played (STATIC/TILT/PRESSURE/KINEMATIC/TEST): ')
        globalS = raw_input('Global score (0-1): ')
        staticS = raw_input('Static score (0-1): ')
        pressureS = raw_input('Pressure score (0-1): ')
        tiltS = raw_input('Tilt score (0-1): ')
        kinematicS = raw_input('Kinematic score (0-1): ')
        level = raw_input('Level (1, 2, 3, 4, 5): ')
        duration = raw_input('Duration of the activity (in sec): ')
        result = raw_input('Outcome (w/f): ')
        sql_command = """INSERT INTO dynamico_table
                         (fname, lname, language, gender, age, left_right, country, city, activity, globalS, staticS, pressureS, tiltS, kinematicS, level, duration, result)
                         VALUES
                         ("%s", "%s", "%s", "%s", %s, "%s", "%s", "%s", "%s", %s, %s, %s, %s, %s, %s, %s, "%s");""" % (fname, lname, language, gender, age, left_right, country, city, activity, globalS, staticS, pressureS, tiltS, kinematicS, level, duration, result)
        cursor.execute(sql_command)
        connection.commit()
        print(cursor.rowcount, "CUSTOM activity record inserted.")
    # add a record related to a test
    else:
        sql_command = """INSERT INTO dynamico_table
                         (fname, lname, language, gender, age, left_right, country, city, activity, globalS, staticS, pressureS, tiltS, kinematicS)
                         VALUES
                         ("Dorsa", "Safaei", "en-GB", "f", 29, "r","iran", "tehran", "test", RAND(), RAND(), RAND(), RAND(), RAND());"""
        cursor.execute(sql_command)
        connection.commit()
        print(cursor.rowcount, "TEST record inserted.")


# display the latest record in the fakedynamico database
def getLastRecord(cursor):
    sql_command = "SELECT * FROM dynamico_table ORDER BY id DESC LIMIT 1"
    cursor.execute(sql_command)
    record = cursor.fetchall()
    print(record)


# display all records in the fakedynamico database
def getAllRecords(cursor):
    sql_command = "SELECT * FROM dynamico_table"
    cursor.execute(sql_command)
    records = cursor.fetchall()
    for row in records:
        print(row)


# display the fields of the dynamico table in the fakedynamico database
def getFields(cursor):
    sql_command = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'dynamico_table'"
    cursor.execute(sql_command)
    records = cursor.fetchall()
    for row in records:
        # only display the name of the field
        print(row[3])


# clear the table content of the fakedynamico database
def clearTable(connection, cursor):
    sql_command = "DELETE FROM dynamico_table"
    cursor.execute(sql_command)
    connection.commit()
    print(cursor.rowcount, "record(s) deleted")


#########################################################################
if __name__ == '__main__':
    # establish connection with the fakedynamico DB
    connection, cursor = connectDB()

    # get user input
    command = commandMenu()

    while 1:
        # switch for the commands
        if command == "WIN" or command == "FAIL" or command == "CSTA" or command == "CSTT" or command == "CST" or command == "TEST":
            addRecord(connection, cursor, command)
        elif command == "LAST":
            getLastRecord(cursor)
        elif command == "ALL":
            getAllRecords(cursor)
        elif command == "DEL":
            deleteTable(cursor)
        elif command == "COLS":
            getFields(cursor)
        elif command == "CLEAR":
            clearTable(connection, cursor)
        else:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
                sys.exit()

        command = commandMenu()