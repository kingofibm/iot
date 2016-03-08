#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv/
import time
import RPi.GPIO as GPIO
from array import *
import datetime

GPIO.setmode(GPIO.BCM)

powerList = []
powerList.append (1)
powerList.append (1)
Told=time.time()
f=open('./mydata.txt','a')
i=1


print GPIO.VERSION
# GPIO 24 set up as input. It is pulled up to stop false signals
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# now the program will do nothing until the signal on port 24
# starts to fall towards zero. This is why we used the pullup
# to keep the signal high and prevent a false interrupt


while (True):
   try:
       print "inne i wait igen"
       i=i+1
       GPIO.wait_for_edge(24, GPIO.FALLING)
       Tnew=time.time()
       frequency=1/(Tnew-Told)
       powerList.append(frequency*3.6)
       Pavg = round((powerList[i]+powerList[i-1]+powerList[i-2])/3,3)
       print "Momentan effekt forbrukning kw/h",Pavg,'   Estimated Cost /m',Pavg*24*30
       Told=Tnew
       f.write(datetime.datetime.now().strftime("20%y-%m-%d %H:%M:%S"))
       f.write(' ')
       f.write(str(Pavg))
       f.write('\n')
   except RuntimeError:
            print "test runtime error"
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
            GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            #f.close()      
  
