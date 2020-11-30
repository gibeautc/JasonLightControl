#!/usr/bin/env python3

# External module imports
import RPi.GPIO as GPIO
import time
import os
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	#client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	if msg.topic=="home/outside/light1/set":
		if msg.payload=="1":
			client.publish("home/outside/light1/status",payload="1")
			GPIO.output(light1,GPIO.LOW)
		else:
			client.publish("home/outside/light1/status",payload="0")	
			GPIO.output(light1,GPIO.HIGH)
	elif msg.topic=="home/outside/light2/set":
		if msg.payload=="1":
			client.publish("home/outside/light2/status",payload="1")
			GPIO.output(light2,GPIO.LOW)
		else:
			client.publish("home/outside/light2/status",payload="0")
			GPIO.output(light2,GPIO.HIGH)
	elif msg.topic=="home/outside/light3/set":
		if msg.payload=="1":
			client.publish("home/outside/light3/status",payload="1")
			GPIO.output(light3,GPIO.LOW)
		else:
			client.publish("home/outside/light3/status",payload="0")
			GPIO.output(light3.GPIO.HIGH)
	elif msg.topic=="home/outside/light4/set":
		if msg.payload=="1":
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


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

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


