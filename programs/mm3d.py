#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.1 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018 Pozsar Zsolt <pozsar.zsolt@.szerafingomba.hu>           |
# | mm3d.py                                                                    |
# | Main program                                                               |
# +----------------------------------------------------------------------------+
#
#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

import ConfigParser
import daemon
import io
import os
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import gmtime, strftime
sys.path.append ('/home/mm3d/programs/')
import prg_current as CR

# load configuration
def loadconfiguration(conffile):
  global logfile
  global lockfile
  try:
    with open(conffile) as f:
      sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    logfile=config.get('directories', 'dir_log')+'mm3d.log'
    lockfile=config.get('directories', 'dir_lck')+'mm3d.lck'
  except:
    print("ERROR: Cannot open configuration file!");

# create and remove lock file
def lckfile(mode):
  try:
    if mode > 0:
      lcf=open(lockfile,'w')
      lcf.close()
    else:
      os.remove(lockfile)
  except:
    print("WARNING: Cannot create/remove lock file!")

# write data to log with timestamp
def writelog(temperature,humidity,inputs,outputs):
  dt=(strftime("%Y-%m-%d,%H:%M", gmtime()))
  lckfile(1)
  try:
    with open(logfile, "r+") as f:
      first_line = f.readline()
      lines = f.readlines()
      f.seek(0)
      f.write(dt+','+str(temperature)+','+str(humidity)+','+
              inputs[0]+','+inputs[1]+','+inputs[2]+','+inputs[3]+','+
              outputs[0]+','+outputs[1]+','+outputs[2]+','+outputs[3]+','+
              outputs[4]+','+outputs[5]+','+outputs[6]+','+outputs[7]+'\n')
      f.write(first_line)
      f.writelines(lines)
      f.close()
  except:
    print("ERROR: Cannot create/write log file!");
  lckfile(0)

# initializing ports
def initports():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(2,GPIO.IN)                         # input #1
  GPIO.setup(3,GPIO.IN)                         # input #2
  GPIO.setup(4,GPIO.IN)                         # input #3
  GPIO.setup(9,GPIO.OUT,initial=GPIO.HIGH)      # output #4
  GPIO.setup(10,GPIO.OUT,initial=GPIO.HIGH)     # output #3
  GPIO.setup(14,GPIO.OUT,initial=GPIO.HIGH)     # error light #1
  GPIO.setup(15,GPIO.OUT,initial=GPIO.HIGH)     # error light #2
  GPIO.setup(17,GPIO.IN)                        # input #4
  GPIO.setup(18,GPIO.OUT,initial=GPIO.HIGH)     # error light #3
  GPIO.setup(22,GPIO.OUT,initial=GPIO.HIGH)     # output #2
  GPIO.setup(23,GPIO.OUT,initial=GPIO.HIGH)     # error light #4
  GPIO.setup(24,GPIO.OUT,initial=0)             # ACT LED
  GPIO.setup(27,GPIO.OUT,initial=GPIO.HIGH)     # output #1

# blink ACT LED
def blinkactled():
  GPIO.output(24,1)
  time.sleep(0.5)
  GPIO.output(24,0)
  time.sleep(0.5)

# main program
loadconfiguration('/usr/local/etc/mm3d/mm3d.ini')
initports()
first=1
prevtemperature=0
prevhumidity=0
previnputs=""
prevoutputs=""
with daemon.DaemonContext() as context:
  try:
    while True:
      sensor=Adafruit_DHT.DHT22
      pin=11
      shum,stemp=Adafruit_DHT.read_retry(sensor,pin)
      humidity=int(shum)
      temperature=int(stemp)
      blinkactled()
      # read input data from GPIO
      inputs=str(int(not GPIO.input(2)))
      inputs=inputs + str(int(not GPIO.input(3)))
      inputs=inputs + str(int(not GPIO.input(4)))
      inputs=inputs + str(int(not GPIO.input(17)))
      blinkactled()
      # run user's function
      outputs=CR.control(temperature,humidity,inputs)
      aop1=CR.autooffport1()
      blinkactled()
      # write output data to GPIO
      GPIO.output(14,not int(outputs[4]))
      GPIO.output(15,not int(outputs[5]))
      GPIO.output(18,not int(outputs[6]))
      GPIO.output(23,not int(outputs[7]))
      GPIO.output(27,not int(outputs[0]))
      GPIO.output(22,not int(outputs[1]))
      GPIO.output(10,not int(outputs[2]))
      GPIO.output(9,not int(outputs[3]))
      if aop1 != "0":
        for i in range(int(aop1)):
          blinkactled()
        GPIO.output(27,1)
      blinkactled()
      # write logfile if changed
      enablewritelog=0
      if prevtemperature!=temperature:
        enablewritelog=1
      if prevhumidity!=humidity:
        enablewritelog=1
      if previnputs!=inputs:
        enablewritelog=1
      if prevoutputs!=outputs:
        enablewritelog=1
      if first==1:
        enablewritelog=1
      if enablewritelog==1:
        first=0
        writelog(temperature,humidity,inputs,outputs)
        prevtemperature=temperature
        prevhumidity=humidity
        previnputs=inputs
        prevoutputs=outputs
      blinkactled()
      # wait 10s
      time.sleep(10)
  except KeyboardInterrupt:
    GPIO.cleanup
exit(0)
