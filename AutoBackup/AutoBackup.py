import os
import datetime
import subprocess
import socket
import sys

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
        print('I got the lock')
    except socket.error:
        print('Lock exists')
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

# Weekly
line = file.readline()
weeklyDate = line
assert "datetime.datetime" in line, "Must contain datetime object in datetime file"
date = eval(file.readline())
if datetime.datetime.now() > date + datetime.timedelta(7):
    print("Weekly Backup Running")
    subprocess.run([os.path.join(cwd, "AutoBackup.weekly")])
    weeklyDate = datetime.datetime.now() 

# Monthly
line = file.readline()
monthlyDate = line
assert "datetime.datetime" in line, "Must contain datetime object in datetime file"
date = eval(file.readline())
if datetime.datetime.now() > date + datetime.timedelta(30):
    print("Monthly Backup Running")
    subprocess.run([os.path.join(cwd, "AutoBackup.monthly")])
    monthlyDate = datetime.datetime.now()

# Monthly
line = file.readline()
bimonthlyDate = line
assert "datetime.datetime" in line, "Must contain datetime object in datetime file"
date = eval(file.readline())
if datetime.datetime.now() > date + datetime.timedelta(60):
    print("Bimonthly Backup Running")
    subprocess.run([os.path.join(cwd, "AutoBackup.bimonthly")])
    bimonthlyDate = datetime.datetime.now()

# Yearly
line = file.readline()
yearlyDate = line
assert "datetime.datetime" in line, "Must contain datetime object in datetime file"
date = eval(file.readline())
if datetime.datetime.now() > date + datetime.timedelta(365):
    print("Yearly Backup Running")
    subprocess.run([os.path.join(cwd, "AutoBackup.yearly")])
    yearlyDate = datetime.datetime.now()

file.close()

print("Writing to backup")
with open("lastBackup.txt", "w") as file:
    file.writelines(repr(weeklyDate) + "\n")
    file.writelines(repr(monthlyDate) + "\n")
    file.writelines(repr(bimonthlyDate) + "\n")
    file.writelines(repr(yearlyDate) + "\n")
