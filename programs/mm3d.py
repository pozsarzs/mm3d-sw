#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.2 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018-2019 Pozsar Zsolt <pozsar.zsolt@.szerafingomba.hu>      |
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
  global prt_act
  global prt_err1
  global prt_err2
  global prt_err3
  global prt_err4
  global prt_in1
  global prt_in2
  global prt_in3
  global prt_in4
  global prt_sens
  global prt_out1
  global prt_out2
  global prt_out3
  global prt_out4
  global sensor
  try:
    with open(conffile) as f:
      sample_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    logfile=config.get('directories', 'dir_log')+'mm3d.log'
    lockfile=config.get('directories', 'dir_lck')+'mm3d.lck'
    prt_act=int(config.get('ports','prt_act'))
    prt_err1=int(config.get('ports','prt_err1'))
    prt_err2=int(config.get('ports','prt_err2'))
    prt_err3=int(config.get('ports','prt_err3'))
    prt_err4=int(config.get('ports','prt_err4'))
    prt_in1=int(config.get('ports','prt_in1'))
    prt_in2=int(config.get('ports','prt_in2'))
    prt_in3=int(config.get('ports','prt_in3'))
    prt_in4=int(config.get('ports','prt_in4'))
    prt_sens=int(config.get('ports','prt_sens'))
    prt_out1=int(config.get('ports','prt_out1'))
    prt_out2=int(config.get('ports','prt_out2'))
    prt_out3=int(config.get('ports','prt_out3'))
    prt_out4=int(config.get('ports','prt_out4'))
    sensor_type=config.get('sensors','sensor_type')
    if sensor_type=='AM2302':
      sensor=Adafruit_DHT.AM2302
    if sensor_type=='DHT11':
      sensor=Adafruit_DHT.DHT11
    if sensor_type=='DHT22':
      sensor=Adafruit_DHT.DHT22
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
  GPIO.setup(prt_act,GPIO.OUT,initial=0)
  GPIO.setup(prt_err1,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(prt_err2,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(prt_err3,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(prt_err4,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(prt_in1,GPIO.IN)
  GPIO.setup(prt_in2,GPIO.IN)
  GPIO.setup(prt_in3,GPIO.IN)
  GPIO.setup(prt_in4,GPIO.IN)
  GPIO.setup(prt_out1,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(prt_out2,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(prt_out3,GPIO.OUT,initial=GPIO.HIGH)
  GPIO.setup(prt_out4,GPIO.OUT,initial=GPIO.HIGH)

# blink ACT LED
def blinkactled():
  GPIO.output(prt_act,1)
  time.sleep(0.5)
  GPIO.output(prt_act,0)
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
      # read input data from sensor
      shum,stemp=Adafruit_DHT.read_retry(sensor,prt_sens)
      humidity=int(shum)
      temperature=int(stemp)
      blinkactled()
      if humidity<100:
        wrongvalues=0
      else:
        wrongvalues=1
      # read input data from GPIO
      inputs=str(int(not GPIO.input(prt_in1)))
      inputs=inputs + str(int(not GPIO.input(prt_in2)))
      inputs=inputs + str(int(not GPIO.input(prt_in3)))
      inputs=inputs + str(int(not GPIO.input(prt_in4)))
      blinkactled()
      # run user's function
      outputs=CR.control(temperature,humidity,inputs,wrongvalues)
      aop1=CR.autooffport1()
      blinkactled()
      # write output data to GPIO
      GPIO.output(prt_err1,not int(outputs[4]))
      GPIO.output(prt_err2,not int(outputs[5]))
      GPIO.output(prt_err3,not int(outputs[6]))
      GPIO.output(prt_err4,not int(outputs[7]))
      GPIO.output(prt_out1,not int(outputs[0]))
      GPIO.output(prt_out2,not int(outputs[1]))
      GPIO.output(prt_out3,not int(outputs[2]))
      GPIO.output(prt_out4,not int(outputs[3]))
      if aop1 != "0":
        for i in range(int(aop1)):
          blinkactled()
        GPIO.output(prt_err3,1)
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
