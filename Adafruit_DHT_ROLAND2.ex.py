#!/usr/bin/env python
# AM2302 Error Checking Script Copyright 2012 Aaron Goeglein <audioscience@gmail.com>
# This script checks the AM2302(DH22) for readings that are 15 degrees/percent over or under the last reading and eliminates them as errors
# and re-checks the sensors
# AM2302 Temperature script derived from Adafruit http://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/
# json->cosm porttion derived from cosm.py Copyright 2012 Itxaka Serrano Garcia <itxakaserrano@gmail.com>
# licensed under the GPL2
# see the full license at http://www.gnu.org/licenses/gpl-2.0.txt
#
# This script will read your AM2302 temperature/humidity then upload the data to cosm.com
# You only need to add 2 things for Cosm, YOUR_API KEY HERE and YOUR_FEED_NUMBER_HERE
# also, you can change your stream ids, in that case change the id names in the "data = json.dumps..." line

import time
import os
import RPi.GPIO as GPIO
import json
import subprocess
import re
import sys

GPIO.setmode(GPIO.BCM)

while True:

        # Run the DHT program to get the humidity and temperature readings for AM2302, replace "2302" with type other than 2302 and "23" with your GPIO pin#

        output = subprocess.check_output(["/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_DHT_Driver/Adafruit_DHT", "2302", "4"]);
        print output
        # search for temperature printout
        matches = re.search("Temp =s+([0-9.]+)", output)
        if (not matches):
          time.sleep(3)
          continue
        temp = float(matches.group(1)) * 1.8 + 32
        temp = round(temp, 2)

        # search for humidity printout
        matches = re.search("Hum =s+([0-9.]+)", output)
        if (not matches):
          time.sleep(3)
          continue
        humidity = float(matches.group(1))
        humidity = round(humidity, 2)

        print "Temperature: %.1f F" % temp
        print "Humidity:    %.1f %%" % humidity

        tfile = open("/home/pi/scripts/last_temp")
        text = tfile.read()
        tfile.close()
        last_temp = text.split()[1]
        last_humid = text.split()[3]

        print last_temp, last_humid

        if temp >= float(last_temp) + 15:
            print "Temp read error"
            time.sleep(3)
            continue

        elif temp <= float(last_temp) - 15:
            print "Temp read error"
            time.sleep(3)
            continue

        elif humidity >= float(last_humid) + 15:
            print "Humidity read error"
            time.sleep(3)
            continue

        elif humidity <= float(last_humid) - 15:
            print "Humidity read error"
            time.sleep(3)
            continue

        tfile = open("/home/pi/scripts/last_temp", 'w')
        tfile.write("Temperature: %.1f " % temp)
        tfile.write( "Humidity:    %.1f" % humidity)
        tfile.close()

        data = json.dumps({"version":"1.0.0", "datastreams":[{"id":"Air_Temperature","current_value":temp},{"id":"Humidity","current_value":humidity}]})
        with open("temp.tmp", "w") as f:
            f.write(data)

 #       subprocess.call(['curl --request PUT --data-binary @temp.tmp --header "X-ApiKey:YOUR_API KEY HERE" http://api.cosm.com/v2/feeds/YOUR_FEED_NUMBER_HERE'], shell=True)

        os.remove("temp.tmp")
        break
