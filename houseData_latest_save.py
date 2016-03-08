#!/usr/bin/env python2.7
import time
from Adafruit_CharLCD_N import Adafruit_CharLCD
import RPi.GPIO as GPIO
from array import *
import datetime
import MySQLdb
from Adafruit_BMP085 import BMP085
import time
import subprocess
import re
import sys

class readDHT:
    def temp(self, ch):
          done =False
          while(not done):
            output = subprocess.check_output(["./Adafruit_DHT", "2302", ch]);
            matches = re.search("Temp =\s+([0-9.]+)", output)
            if (not matches):
               time.sleep(1)
               continue
            done = True
          temp = float(matches.group(1))
          return temp

    def hum(self, ch):
          done =False
          while(not done):
            output = subprocess.check_output(["./Adafruit_DHT", "2302", ch]);
            matches = re.search("Hum =\s+([0-9.]+)", output)
            if (not matches):
               time.sleep(1)
               continue
            done = True
          Hum = float(matches.group(1))
          return Hum


bmp = BMP085(0x77)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode


GPIO.setmode(GPIO.BCM)
powerList = [0]*10
Told=time.time()
latestLog = time.time()
lcd = Adafruit_CharLCD()
lcd.clear()
lcd.begin(20,4)
i=0

con = MySQLdb.connect('localhost','pi','','house');
cursor = con.cursor()

x = readDHT()

# GPIO 18 set up as input for power sensor . It is pulled up to stop false signals
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# GPIO 7 set up as input for humidity sensor 1

while (True):
 
   try:
       while GPIO.input(18)==GPIO.HIGH:
             time.sleep(0.00001)
       Tnew=time.time()
       frequency=1/(Tnew-Told)
       powerList[0]=frequency*3.6
       Pavg = round((powerList[0]),3)
       Told=Tnew
#       print "Momentan effekt forbrukning ute loop kw/h",Pavg,'   Estimated Cost /m',Pavg*24*3

       if (time.time()-latestLog > 30):
           
           # read from BMP085 
           tempBmp = bmp.readTemperature()
           pressure = bmp.readPressure()

           #read from humidity sensor 1 on GPIO pin  7  (CE00)
           temp = x.temp("7")
           humidity = x.hum("7")

#           read from humidity sensor 2 in pin 4
           tempS2=x.temp("4")
           humidityS2=x.hum("4")

           lcd.messageN("Power Usage %.3f" % Pavg,1)
           lcd.messageN("Humidity %.1f/%.1f " % (humidity,humidityS2),2)
           lcd.messageN("Preassure %.0f hPa" % (pressure/100.0)  ,3)
           lcd.messageN("Temp %.1f/%.1f/%.1f " % (round(temp,0),tempBmp,tempS2),4)
           latestLog = time.time()
           cursor.execute("INSERT INTO housedata (date, power,temp,humidity,tempS2,humidityS2) "
                     "VALUES(%s, %s,%s,%s,%s,%s)",
                     (str(datetime.datetime.now()), str(Pavg), str(temp),str(humidity),str(tempS2),str(humidityS2)))
          
           con.commit() 

       time.sleep(0.04)
   except KeyboardInterrupt:
            cursor.close()
            con.close()
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
  

