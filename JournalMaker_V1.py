#!/usr/bin/env python

import os, time, shelve

# Notes: make GUI for this program
#        Make sure timezone is correct

path = '/Users/WillC/Documents/Rutgers/Aresty_SSP/Daily Logs/';
os.chdir(path);

date = time.strftime("%Y_%m_%d", time.gmtime());
month = time.strftime("%B", time.gmtime());
day = time.strftime("%d", time.gmtime());
year = time.strftime("%Y", time.gmtime());

secondsDay = 86400
prevDays = 1;
yesterday = time.strftime("%Y_%m_%d", time.gmtime(time.time() - prevDays*secondsDay));

# Keeps track of numday of current experiment
def getNumDay():
    c = shelve.open('JournalTracker');
    numDay = c['Direct Imaging of Au-doped FePn'];
    c['Direct Imaging of Au-doped FePn'] += 1;
    c.close()
    return numDay;

def logName(day = date):
    return "Log_" + day + ".txt";

def checkExist(name):
    for i in os.listdir():
        if(i == name):
            return True;
    return False;

def extractToDo(prevDays, yesterday):
    count = 0
    for i in os.listdir():
        count += 1;

    # Finds last created log
    exists = False;
    while (prevDays < count):
        yesterday = time.strftime("%Y_%m_%d", time.gmtime(time.time() - prevDays*secondsDay));
        prevDays += 1;
        if (checkExist(logName(yesterday)) == True):
            prevlog = logName(yesterday);
            exists = True;
            break;

    if (exists == False):
        return ""; 
    file = open(prevlog, 'r');
    search = file.read()
    index = search.find("To-do:") + 6; # Goes to the first line after "To-do:"
    extract = search[index:];
    file.close();
    return extract;

def createLog():
    exist = checkExist(logName()); # assign to checkExist()
    if (exist == True):
        print("Your text file already exists!");
        return False;
    else:
        oneline = "Date: " + month + " " + day + ", " + year;
        twoline = "\n\nDay #" + str(getNumDay()) + " of Direct Imaging of Gold-doped Iron Pnictides (BaFe2As2) with Laser Illumination";
        progress = "\n\nProgress:";
        todo = "\n\nTo-do:" + extractToDo(prevDays, yesterday);

        # opens a new log and writes the template onto it
        log = open(logName(), 'w');
        log.write(oneline + twoline + progress + todo);
        log.close();
        
        print("Your log has been created for " + date);
        return True;

createLog();
