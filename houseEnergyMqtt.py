#!/usr/bin/env python2.7

import paho.mqtt.client as mqtt
import json
import uuid

import time
import RPi.GPIO as GPIO
from array import *
import datetime
import time
import subprocess
import re
import sys
from pytz import timezone
import pytz


i=0

#Set the variables for connecting to the iot service
broker = ""
topic = "iot-2/evt/d/fmt/json"
username = "use-token-auth"


password = "12345678" #auth-token
organization = "dk21wt" #org_id
deviceType = "PiEnergy"
deviceId = "PiEnergy"


topic = "iot-2/evt/d/fmt/json"

#Creating the client connection
#Set clientID and broker
clientID = "d:" + organization + ":" + deviceType + ":" + deviceId
broker = organization + ".messaging.internetofthings.ibmcloud.com"
mqttc = mqtt.Client(clientID)

#Set authentication values, if connecting to registered service
if username is not "":
 mqttc.username_pw_set(username, password=password)
mqttc.connect(host=broker, port=1883, keepalive=60)


# Set correct time zone 
sweden = timezone('Europe/Amsterdam')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
powerList = [0]*10
Told=time.time()
latestLog = time.time()
i=0

# GPIO 18 set up as input for power sensor . It is pulled up to stop false signals
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Publishing to IBM Internet of Things Foundation
mqttc.loop_start()

while (True):
  
   try:
       while GPIO.input(18)==GPIO.HIGH:
             print ("waiting")
             time.sleep(0.00001)
             
       
       Tnew=time.time()
       frequency=1/(Tnew-Told)
       powerList[0]=frequency*3.6
       Pavg = round((powerList[0]),3)
       Told=Tnew

       if (time.time()-latestLog > 10):
           latestLog = time.time()
           msg = json.JSONEncoder().encode({"d":{"cpuutil":i}})
           mqttc.publish(topic, payload=msg, qos=0, retain=False)
           print (Pavg)
           time.sleep(0.5)

       time.sleep(0.04)
   except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
  

