#!/usr/bin/env python3

# External module imports
import RPi.GPIO as GPIO
import time
import os
import paho.mqtt.client as mqtt
from os import path


PIDFILE="/home/pi/.light.pid"
PASSWORDFILE="/home/pi/.password"

def GetBrokerPassword():
	if not path.exists(PASSWORDFILE):
		print("No Password File")
		exit()
	else:
		f=open(PASSWORDFILE,"r")
		return f.read()


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


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

def on_disconect(client,userdata,rc):
	print("Got Disconnect from broker:"+str(rc))
	time.sleep(5)
	client.reconnect()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	pl=int(msg.payload)
	if msg.topic=="home/outside/light1/set": 
		if pl==1:
			client.publish("home/outside/light1/status",payload="1")
			GPIO.output(light1,GPIO.LOW)
		else:
			client.publish("home/outside/light1/status",payload="0")	
			GPIO.output(light1,GPIO.HIGH)
	elif msg.topic=="home/outside/light2/set":
		if pl==1:
			client.publish("home/outside/light2/status",payload="1")
			GPIO.output(light2,GPIO.LOW)
		else:
			client.publish("home/outside/light2/status",payload="0")
			GPIO.output(light2,GPIO.HIGH)
	elif msg.topic=="home/outside/light3/set":
		if pl==1:
			client.publish("home/outside/light3/status",payload="1")
			GPIO.output(light3,GPIO.LOW)
		else:
			client.publish("home/outside/light3/status",payload="0")
			GPIO.output(light3,GPIO.HIGH)
	elif msg.topic=="home/outside/light4/set":
		if pl==1:
			client.publish("home/outside/light4/status",payload="1")
			GPIO.output(light4,GPIO.LOW)
		else:
			client.publish("home/outside/light4/status",payload="0")
			GPIO.output(light4,GPIO.HIGH)
	else:
		print("unknown topic:",msg.topic)


def measure_temp():
		temp = os.popen("vcgencmd measure_temp").readline()
		return (temp.replace("temp=",""))


DoWatchDog()

fileC=GetBrokerPassword()
fileC=fileC.split(":")
username=fileC[0].strip()
password=fileC[1].strip()

client = mqtt.Client()
print("Using Username:",username)
print("password:",password)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect=on_disconect
client.username_pw_set(username, password=password)
client.connect("localhost", 1883, 60)
client.subscribe("home/outside/light1/set",0)
client.subscribe("home/outside/light2/set",0)
client.subscribe("home/outside/light3/set",0)
client.subscribe("home/outside/light4/set",0)

# Pin Definitons:
light1=4
light2=17
light3=27
light4=22
#pwmPin = 18 # Broadcom pin 18 (P1 pin 12)
#ledPin = 23 # Broadcom pin 23 (P1 pin 16)
#butPin = 17 # Broadcom pin 17 (P1 pin 11)

#dc = 95 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(light1, GPIO.OUT) # LED pin set as output
GPIO.setup(light2, GPIO.OUT) # PWM pin set as output
GPIO.setup(light3, GPIO.OUT)
GPIO.setup(light4, GPIO.OUT)

#pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
#GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

# Initial state for LEDs:
GPIO.output(light1, GPIO.HIGH)
GPIO.output(light2,GPIO.HIGH)
GPIO.output(light3,GPIO.HIGH)
GPIO.output(light3,GPIO.HIGH)


print("Here we go! Press CTRL+C to exit")
lastCheck=time.time()
state=True
try:
	while 1:
		client.loop()
		if time.time()-lastCheck>5:
			client.publish("pi/temp", measure_temp())
			lastCheck=time.time()

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	GPIO.cleanup() # cleanup all GPIO


