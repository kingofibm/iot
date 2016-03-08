
#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv/
import time
import RPi.GPIO as GPIO
from array import *
import datetime
import MySQLdb
from Adafruit_BMP085 import BMP085
import time
bmp = BMP085(0x77)

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode


GPIO.setmode(GPIO.BCM)
powerList = [0]*10000
Told=time.time()

f=open('./mydata.txt','a')
i=0

# GPIO 24 set up as input. It is pulled up to stop false signals
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# now the program will do nothing until the signal on port 24
# starts to fall towards zero. This is why we used the pullup
# to keep the signal high and prevent a false interrupt

con = MySQLdb.connect('localhost','pi','','house');
cursor = con.cursor()

while (True):
   try:
       while GPIO.input(24)==GPIO.HIGH:
             time.sleep(0.0001)
       Tnew=time.time()
       frequency=1/(Tnew-Told)
       powerList[i]=frequency*3.6
       Pavg = round((powerList[0]+powerList[1]+powerList[2])/3,3)
       print "Momentan effekt forbrukning kw/h",Pavg,'   Estimated Cost /m',Pavg*24*30
       Told=Tnew
       temp = bmp.readTemperature()
       pressure = bmp.readPressure()
       altitude = bmp.readAltitude()

       print "Temperature: %.2f C" % temp
       print "Pressure:    %.2f hPa" % (pressure / 100.0)
       print "Altitude:    %.2f" % altitude

#       cursor.execute("insert into housedata(date,power) values(datetime.datetime.now(),i)")
#       cursor.execute("INSERT INTO housedata (date, power,temp) "
#                    "VALUES(%s, %s,%s)",
#                    (str(datetime.datetime.now()), str(Pavg), str(temp)))
       con.commit() 

       time.sleep(0.02)
       if i>=2:
          i=0
       else :
          i+=1
   except KeyboardInterrupt:
            cursor.close()
            con.close()
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
            f.close()      
  
