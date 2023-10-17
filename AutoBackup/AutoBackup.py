#!/usr/bin/python3
import os
import re
import sys
import datetime
import subprocess
import socket

print("Starting Script")
# Verify that the process isn't already running
def get_lock(process_name):
    # Without holding a reference to our socket somewhere it gets garbage
    # collected when the function exits
    get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:
        # The null byte (\0) means the socket is created 
        # in the abstract namespace instead of being created 
        # on the file system itself.
        # Works only in Linux
        get_lock._lock_socket.bind('\0' + process_name)
        print('Sucessfuly Obtained Lock')
    except socket.error:
        print('Lock Exists')
        sys.exit()

get_lock('running_dropbox_backup')

try:
    file = open("lastBackup.txt", "r")
    print("Opened Last Backup file")
except FileNotFoundError:
    print("Generating Last Backup file")
    weeklyDate = datetime.datetime.now() - datetime.timedelta(7)
    monthlyDate = datetime.datetime.now() - datetime.timedelta(30)
    bimonthlyDate = datetime.datetime.now() - datetime.timedelta(60)
    yearlyDate = datetime.datetime.now() - datetime.timedelta(365)
    
    with open("lastBackup.txt", "w") as file:
        file.writelines(repr(weeklyDate) + "\n")
        file.writelines(repr(monthlyDate) + "\n")
        file.writelines(repr(bimonthlyDate) + "\n")
        file.writelines(repr(yearlyDate) + "\n")

    file = open("lastBackup.txt", "r")

cwd = os.getcwd()

timeframe = ["weekly", "monthly", "bimonthly", "yearly"]
timeframedays = [7, 30, 60, 365]
lastUpdated = [None, None, None, None]

for t in range(len(timeframe)):
    tf = timeframe[t]
    tfd = timeframedays[t]
    line = file.readline()
    lastUpdated[t] = line
    assert "datetime.datetime" in line, "Must contain datetime object in lastBackup.txt file"
    assert re.search("^datetime\.datetime\((\d+, ){6}\d+\)$", line), "Must contain datetime object in lastBackup.txt file"
    date = eval(file.readline())
    if datetime.datetime.now() > date + datetime.timedelta(tfd):
        print(f"{tf} Backup Running")
        subprocess.run([os.path.join(cwd, f"AutoBackup.{tf}")])
        lastUpdated[t] = datetime.datetime.now() 
    #raise RuntimeError
file.close()

print("Writing to backup")
with open("lastBackup.txt", "w") as file:
    for date in lastUpdated:
        file.writelines(repr(date) + "\n")
