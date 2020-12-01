#!/usr/bin/env python3


import os 
import time
from os import path

PIDFILE=".light.pid"

def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def DoWatchDog():
	if not path.exists(PIDFILE):
		print("No Pid File, writing new one")
		f=open(PIDFILE,'w')
		f.write(str(os.getpid()))
		f.close()
		return
	else:
		print("PID exists, need to check it")
		f=open(PIDFILE,'r')
		fileContents=f.read()
		f.close()
		existingPid=int(fileContents)
		print("Existing PID is")
		print(existingPid)
		if check_pid(existingPid):
			print("Existing PID is running")
			exit()
		else:
			print("Existing PID is dead, continuing")
			f=open(PIDFILE,'w')
			f.write(str(os.getpid()))
			f.close()
			
			

DoWatchDog()

while True:
	time.sleep(1)
	print("running")
		
