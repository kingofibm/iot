#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv/
import time
import RPi.GPIO as GPIO
from array import *
import datetime

GPIO.setmode(GPIO.BCM)

powerList = [0]*10

Told=time.time()
f=open('./mydata.txt','a')

i=0

# GPIO 24 set up as input. It is pulled up to stop false signals
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# now the program will do nothing until the signal on port 24
# starts to fall towards zero. This is why we used the pullup
# to keep the signal high and prevent a false interrupt


while (True):
   try:
       GPIO.wait_for_edge(24, GPIO.FALLING)
       Tnew=time.time()
       frequency=1/(Tnew-Told)
       powerList[i]=frequency*3.6
       Pavg = round((powerList[0]+powerList[1]+powerList[2]+powerList[3]+powerList[4]+powerList[5]+powerList[6]+powerList[7]+powerList[8]+powerList[9])/10,3)
       print "Momentan effekt forbrukning kw/h",Pavg,'   Estimated Cost /m',Pavg*24*30
       Told=Tnew
       f.write(datetime.datetime.now().strftime("20%y-%m-%d %H:%M:%S"))
       f.write(' ')
       f.write(str(Pavg))
       f.write('\n')
       if i>=9:
          GPIO.cleanup()
          GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
          i=0
       else :
          i+=1
   except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
            f.close()      
  
