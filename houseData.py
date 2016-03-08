

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

i=0
latestLog=time.time()

# GPIO 24 set up as input. It is pulled up to stop false signals
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# now the program will do nothing until the signal on port 24
# starts to fall towards zero. This is why we used the pullup
# to keep the signal high and prevent a false interrupt

con = MySQLdb.connect('localhost','pi','','house');
cursor = con.cursor()

con = MySQLdb.connect('localhost','pi','','house');
cursor = con.cursor()

while (True):

   try:

       while GPIO.input(24)==GPIO.HIGH:
             time.sleep(0.0001)
             print "waiting "
       Tnew=time.time()
       frequency=1/(Tnew-Told)
       powerList[i]=frequency*3.6
       Pavg = round((powerList[0]+powerList[1]+powerList[2])/3,3)
       if i>=2:
          i=0
       else :
          i+=1
       Told=Tnew

       # get data from BMP085 sensor
       temp = bmp.readTemperature()
       pressure = bmp.readPressure()

       #       Get Data from ADH 2302 sensor
       if (time.time()-latestLog > 10):

           output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);
           matches = re.search("Temp =\s+([0-9.]+)", output)
           if (not matches):
              time.sleep(3)
              continue
           temp = float(matches.group(1))
           # search for humidity printout
           matches = re.search("Hum =\s+([0-9.]+)", output)
           if (not matches):
              time.sleep(3)
              continue
           print "Temperature: %.2f C" % temp
           print "Pressure:    %.2f hPa" % (pressure / 100.0)

           humidity = float(matches.group(1))

           print "Momentan effekt forbrukning kw/h",Pavg,'   Estimated Cost /m',Pavg*24*30
           print "Temperature: %.1f C" % temp
           print "Humidity:    %.1f %%" % humidity
           print str(humidity)
           latestLog = time.time()


           cursor.execute("INSERT INTO housedata (date, power,temp,humidity) "
                     "VALUES(%s, %s,%s,%s)",
                     (str(datetime.datetime.now()), str(Pavg), str(temp),str(humidity)))
           con.commit()
   except KeyboardInterrupt:
            cursor.close()
            con.close()
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    
