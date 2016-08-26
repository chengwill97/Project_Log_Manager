#!/usr/bin/env python3

"""
PURPOSE:
This program allows you to maintain text-only logs for multiple logs using a CSV file to keep track of everything.
Feel free to change the code as you please.
Best of luck!
- William Cheng, RU '19

Work in Progress:
- To-do list is not being copied
- Make GUI for this program
- Add compatability for windows when changing file paths
- Allow directories that do not exist to be created

COMMENTS:
The CSV file created is organized such the each row has three elements and they are

Project Name, Day of the last project log (0 means none has been created), and Project Log Directory
organized in that order.
"""

import os, time, sys, csv, subprocess, traceback

# Very big welcome to anyone who runs this application
version_date = ["2.0", "August 25, 2016"];
print("{0}\nWELCOME to William Cheng's\nProject_Log_Manager Verion {1}\nModified on {2}\n{3}".format(50*"\n" + 10*"*", version_date[0], version_date[1], 10*"*" + 3*"\n"));
time.sleep(1.5);

# IMPORTANT: path must be changed if on a different computer than Will's
path = '/Users/WillC/Documents/Code/python/Project_Log_Manager/';
# IMPORTANT: application is to open the logs is up to you
applicationOpenWith = 'Sublime Text 2';

"""
# Makes sure the directory for the project data base exists
# DONE
"""
def changePath(currPath):
    try:
        os.chdir(currPath);
    except FileNotFoundError:
        print("\nType \"0\" to exit the program.")
        newPath = input("\nPlease enter a valid file path for your personal \"Project_DataBase\"\nFile Path: ");
        if (newPath[-1] != '/'):
            newPath += '/';
        print("Remember to change the path variable in the beginning of this code: \nFrom\n" + path + "\nTo this\n" + newPath);
        if (newPath == "0"):
            print("\nWarping...");
            sys.exit();
        changePath(newPath);
    return;

"""
# Extracts all data from the csv file.
# DONE
"""
def extractCSV():
    dataBase = []; # for when createLog() is called again

    try:
        projectDataBase = open("Project_Database.csv", "rt");
    except FileNotFoundError:
        print("Creating \"Project_DataBase.csv\" in the directory:\n" + path + "\n");
        newDataBase = open("Project_DataBase.csv", "wt");
        newDataBase.close();
        projectDataBase = open("Project_DataBase.csv", "rt");
        
    readDataBase = csv.reader(projectDataBase);
    
    for row in readDataBase:
        dataBase.append(row);

    projectDataBase.close()

    return dataBase;

"""
# Writes dataBase to Project_DataBase.csv and then exits the program
# DONE
"""
def writeToCSV(dataBase): # closes application after calling this
    os.chdir(path);
    projectDataBase = open("Project_DataBase.csv", "wt");
    writeDataBase = csv.writer(projectDataBase);
    for row in dataBase:
        writeDataBase.writerow(row);
    projectDataBase.close();
    print("\nWARPING.........");
    sys.exit();
def writeToCSV_NoExit(dataBase): # does not close application after calling this
    os.chdir(path);
    projectDataBase = open("Project_DataBase.csv", "wt");
    writeDataBase = csv.writer(projectDataBase);
    for row in dataBase:
        writeDataBase.writerow(row);
    projectDataBase.close();

"""
# Will retrieve the project name or create a new one if needed and allows other options
# DONE:
"""
def getProjNameandPath(dataBase):
    countProject = 1;
    showOptions = True;

    print(50*"\n"); # Gives a nice spacing to the code

    print("Current Projects:")
    for row in dataBase:
        if (row[1] == str(0)):
            print(str(countProject) + ". NEW PROJECT: " +  row[0] + "\n\tLocated at: " + row[2]);
        else:
            # Prints out the project options in this format -> Ex. 1. Day # This is the first project\n   Located at: path1\n2. Day # This is the second project \n   Located at: path2
            print(str(countProject) + ". Day " + row[1] + " of " + row[0] + "\n\tLocated at: " + row[2]);
        countProject += 1;
        
    if (countProject == 1):
        print("No projects have been created yet!");
        showOptions = False;
    print("Other Options:");
    # Allows user to add a project to the dataBase
    print(str(countProject) + ". Add a Project!");

    if (showOptions):
        # Allows user to change a project name
        print(str(countProject+1) + ". Change a project name.");

        # Allows user to change a project log's directory
        print(str(countProject+2) + ". Change a project log's directory.");

        # Allows user to update the project's current log number
        print(str(countProject+3) + ". Update a project's current log number.\n\t***Program will update current log number automatically when creating a new project. Only do so if there is a problem.***");

    print("Type \"0\" to exit the program.");
    
    print("^");
    try:
        projectPick = int(input("\nChoose the number of the project you want the log to be created for OR choose the option you want to take.\n"));
    except ValueError:
        print(50*'\n' + "Please enter an integer.\nTeleporting you back to the selection screen...");
        time.sleep(3);
        return getProjNameandPath(dataBase);
    if (str(projectPick) == "0"):
        writeToCSV(dataBase);
    elif (int(projectPick) < 0 or int(projectPick) > countProject+3):
        print("Your input was totally invalid and not one of the options specified, man. I am teleporting you back to the selection screen.");

    if (str(projectPick) == str(countProject)): # Add a new project
        print("Type \"0\" to exit the program.");
        name = input("\nEnter your desired project name:\n"); # Add new project name
        if (str(name) == "0"):
            writeToCSV(dataBase);

        print("Type \"0\" to exit the program.");
        newPath = input("\nEnter your project log's directory:\n"); # Add new project directory
        if (str(newPath) == "0"):
            writeToCSV(dataBase);

        if (len(newPath) > 0 and newPath[-1] != '/'):
            newPath += '/';
                
        dataBase.append([name, "0", newPath]);
        if (input("\nWould you like to go back to the selection? \n\"Yes\" to go back.\nType anything to exit.\n").lower() == "yes"):
            return getProjNameandPath(dataBase);
        else:
            writeToCSV(dataBase);
            
    if (showOptions):
        if (str(projectPick) == str(countProject+1)): # Change a project name
            print("Type \"0\" to exit the program.");
            projectPick = input("\nChoose the project name you would like to edit:\n");
            if (str(projectPick) == "0"):
                writeToCSV(dataBase);
            
            projectName = input("\nWhat would you like the new project name to be?\n");
            if (str(projectPick) == "0"):
                writeToCSV(dataBase);
            dataBase[int(projectPick)-1][0] = projectName;
            
            # Allows user to go back to selection or exit
            if (input("\nWould you like to go back to the selection? \n\"Yes\" to go back.\nType anything to exit.\n").lower() == "yes"):
                return getProjNameandPath(dataBase);
            else:
                writeToCSV(dataBase); 

        if (str(projectPick) == str(countProject+2)): # Change a project log's directory
            print("Type \"0\" to exit the program.");
            projectPick = input("\nChoose the project log's path you would like to edit:\n");
            if (str(projectPick) == "0"):
                writeToCSV(dataBase);

            print("Type \"0\" to exit the program.");
            changePath = input("\nWhat is your desired file path for " + dataBase[int(projectPick)-1][0] + "\n");
            if (str(changePath) == "0"):
                writeToCSV(dataBase);
            if (changePath[-1] != '/'):
                changePath += '/';
            dataBase[int(projectPick)-1][2] = changePath;
            
            # Allows user to go back to selection or exit
            if (input("\nWould you like to go back to the selection? \n\"Yes\" to go back.\nType anything to exit.\n").lower() == "yes"):
                return getProjNameandPath(dataBase);
            else:
                writeToCSV(dataBase); 

        if (str(projectPick) == str(countProject+3)): # Change a project's current day
            print("Type \"0\" to exit the program."); 
            projectPick = input("\nChoose the project whose current day you would like to edit:\n");
            if (str(projectPick) == "0"):
                writeToCSV(dataBase);
            
            pickDay = input("\nWhat would you like to update the log day to for " + dataBase[int(projectPick)-1][0] + ".\nValues 0 or greater are valid\n");
            try:
                if (int(pickDay) < 0):
                    print("Negative days are invalid, sir. Teleporting you back to the selection, sir.");
                    return getProjNameandPath(dataBase);
            except TypeError:
                print("That input is not an integer. Teleporting you back to the selection screen.");
                
            if (logNumChangeValid(projectPick, int(pickDay), dataBase) == False):
                print("This log day has already been created. Please choose another one.\nTeleporting you back to the selection, sir.");
                return getProjNameandPath(dataBase);
            
            dataBase[int(projectPick)-1][1] = pickDay;
            # Allows user to go back to selection or exit
            if (input("\nWould you like to go back to the selection? \n\"Yes\" to go back.\nType anything to exit.\n").lower() == "yes"):
                return getProjNameandPath(dataBase);
            else:
                writeToCSV(dataBase); 

    writeToCSV_NoExit(dataBase);
    
    name = dataBase[int(projectPick)-1][0];
    currDay = dataBase[int(projectPick)-1][1];
    path = dataBase[int(projectPick)-1][2];
    return [name, currDay, path];

"""
# Checks if the file 'name' exists in the directory
# DONE
"""
def checkFullNameExist(name):
    index = name.index("_");
    logCheck = 0;
    dateCheck = 0;
    
    for i in os.listdir():
        if(logCheck == 0 and i[:index] == name[:index]):
            logCheck += 1;
        if(dateCheck == 0 and i[index+1:] == name[index+1:]):
            dateCheck += 2;
    return logCheck + dateCheck;

"""
# Keeps track of numday of current experiment
# DONE
"""
def getNumDay_LogName_checkExist(getProjNameFunction, date, dataBase):
    rowCount = 0;
    numDay = 0;
    
    for row in dataBase: # Finds the project and +1 to the day tracker
        if (row[0] == getProjNameFunction[0]):
            numDay = int(row[1]) + 1;
            break;
        rowCount += 1;

    # gets the name of the log file
    logName = "Log"+ str(numDay) + "_" + date + ".txt";

    # Checks if a file has been created for current numDay before changing the dataBase file
    check = checkFullNameExist(logName);

    if (check == 0):
        dataBase[rowCount][1] = str(numDay);
    
    return [str(numDay), logName, check];

"""
# This will be the file name of your log
# Currently is not used. 
"""
def getLogName(numDay, date):
    # Change the format of the name however you want
    return "Log"+ numDay + "_" + date + ".txt";

"""
# Used in changing a project's current day in the getNameandProjPath() function. Will check if the change if valid or not.
  Validity is certain if
  1. there is no log already with that day in its file name
  2. more to be added
# DONE
"""
def logNumChangeValid(projNum, pickDay, dataBase):
    changeValid = True;
    checkThis = "Log" + str(pickDay + 1);
    os.chdir(dataBase[int(projNum)-1][2]);

    for fileName in os.listdir():
        if (fileName.find(checkThis) != -1):
            changeValid = False;

    os.chdir(path);
    return changeValid;

"""
# Check if the series of logs exists at all in directory. Create new log series if not.
# DONE
"""
def createFirstLogBool(projPath):
    os.chdir(projPath);
    for i in os.listdir():
        if (i[:3] == "Log"):
            return False;   # False means there exists logs for this project already
    return True; # True means there is no logs for this project yet       

"""
# This can extract different things. Currently, it extracts everything after copyAfterThis
# This is good for copying ongoing to-do lists, general information, or whatever the fuck you want
# DONE
"""
def copyLastFile(prevDays, copyAfterThis, secondsDay, numDay):
    count = 0
    for i in os.listdir():
        count += 1;
        
    # Finds last created log
    exists = False;
    while (prevDays < count):
        yesterday = time.strftime("%Y_%m_%d", time.gmtime(time.time() - prevDays*secondsDay-14400));
        prevDays += 1;
        if (checkFullNameExist(getLogName(numDay, yesterday)) > 0):
            numDay = str(int(numDay)-1);
            prevlog = getLogName(numDay, yesterday);
            exists = True;
            break;

    if (exists == False):
        return "";
    try:
        file = open(prevlog, 'r');
        search = file.read()
        index = search.find(str(copyAfterThis)) + 6; # Goes to the first line after "To-do:"
        extract = search[index:];
        file.close();
    except FileNotFoundError:
        print("No previous file found.")
        return "";
    return extract;

"""
# This opens the log file with a desired application
"""
def openFile(logFolder, logFile, app = applicationOpenWith):
    filePath = logFolder + logFile;
    subprocess.Popen(['open', '-a', app, filePath]);
    return;

"""
# This opens a new log with name returns by getLogName() and auto writes what is inside the file
"""
def createLog(dataBase):
    logCreated = False;
    # Set desired file path of Project_DataBase.csv
    changePath(path);
    
    # These few lines sets time variables
    date = time.strftime("%Y_%m_%d", time.localtime());
    # Ex. 2016_08_22
    month = time.strftime("%B", time.localtime());
    # Ex. January
    day = time.strftime("%d", time.localtime());
    # Ex. 23
    year = time.strftime("%Y", time.localtime());
    # Ex. 1997
    
    secondsDay = 86400;
    prevDays = 1;
    
    # Look above
    currDataBase = dataBase;
    projNameandPath = getProjNameandPath(currDataBase);

    # Sets file path of the desired project log
    try:
        os.chdir(projNameandPath[2]);
    except:
        print("Please check that the following directory exists.\nCheck Directory: " + projNameandPath[2]);
        writeToCSV(currDataBase);
        
    numDay_LogName_checkExist = getNumDay_LogName_checkExist(projNameandPath, date, currDataBase);
    numDay, logName, checkName = numDay_LogName_checkExist[0], numDay_LogName_checkExist[1], numDay_LogName_checkExist[2];
    
    # If today's has already been created, output Error
    if (checkName > 0):
        if (checkName == 1):
            print("A log created for this project day, {0}, already exists.".format(str(numDay)));
        elif (checkName == 2):
            print("A log created for this date, {0}, already exists.".format(date));
        elif (checkName == 3):
            print("Your log file already exists!");
        logCreated = False;
        
    # If this is the first ever log in the series, create a new one
    elif (createFirstLogBool(projNameandPath[2]) == True):
        oneline = "Date: " + month + " " + day + ", " + year;
        twoline = "\n\nDay #1 of " + projNameandPath[0];
        progress = "\n\nProgress:";
        todo = "\n\nTo-do:";

        # opens a new log and writes the template onto it
        log = open(logName, 'w');
        log.write(oneline + twoline + progress + todo);
        log.close();
        
        print("\nGOOD LUCK ON YOUR PROJECT!\nYour first log, " + logName + ", has been created.");
        logCreated = True; 
    
    else:
        oneline = "Date: " + month + " " + day + ", " + year;
        twoline = "\n\nDay #" + numDay + " of " + projNameandPath[0];
        progress = "\n\nProgress:";
        todo = "\n\nTo-do:" + copyLastFile(prevDays, "To-do:", secondsDay, numDay);

        # opens a new log and writes the template onto it
        log = open(logName, 'w');
        log.write(oneline + twoline + progress + todo);
        log.close();
        
        print("\nYour log, " + logName + ", has been created.");
        logCreated =  True;

    if (logCreated == True and input('\nOpen file, ' + logName + '?\nThis will also close the application.\nYes or No\n').lower() == 'yes'):
        openFile(projNameandPath[2], logName);
        writeToCSV(currDataBase);

    if (input("\n\nIs there anything else anything you want to do before I travel back to the 7th dimension and exit the program?\nYes or No\n").lower() == "yes"):
        return True;
    else:
        return False;

"""

     START      START      START      START
    PROGRAM    PROGRAM    PROGRAM    PROGRAM

     START      START      START      START
    PROGRAM    PROGRAM    PROGRAM    PROGRAM

     START      START      START      START
    PROGRAM    PROGRAM    PROGRAM    PROGRAM

"""

# Safeguards against losing information in the CSV if an unexpected error occurs
while (True):
    backup_database = extractCSV();
    
    try:
        if (createLog(backup_database) == True):
            continue;
        else:
            print("\nFare well, young scientist.\n Warping.....");
            sys.exit()
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info();
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback);
        print(''.join('' + line for line in lines));
        print("\nAn ERROR has occurred. Please take a look at it before I return for duty again.");
        writeToCSV(backup_database);
    except KeyboardInterrupt:
        print("Emergency EXIT Initiated");
        writeToCSV(backup_database);
        