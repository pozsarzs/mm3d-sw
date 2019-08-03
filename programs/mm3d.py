#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.3 * Growing house controlling and remote monitoring system         |
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

# write a line to logfile
def writetodebuglog(level,text):
  if dbg_log == "1":
    if level == "i":
      lv="INFO   "
    if level == "w":
      lv="WARNING"
    if level == "e":
      lv="ERROR  "
    debugfile = dir_log+time.strftime("debug-%Y%m%d.log")
    dt=(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    try:
      with open(debugfile, "a") as d:
        d.write(dt+'  '+lv+' '+text+'\n')
        d.close()
    except:
      print ""

# load configuration
def loadconfiguration(conffile):
  global dbg_log
  global dir_log
  global dir_var
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
    dbg_log='0'
    dbg_log=config.get('others', 'dbg_log')
    dir_log=config.get('directories', 'dir_log')
    dir_var=config.get('directories', 'dir_var')
    logfile=dir_log+'mm3d.log'
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
    writetodebuglog("i","Starting program as daemon.")
    writetodebuglog("i","Configuration is loaded.")
  except:
    writetodebuglog("e","Cannot open " + conffile + "!")

# create and remove lock file
def lckfile(mode):
  try:
    if mode > 0:
      lcf=open(lockfile,'w')
      lcf.close()
      writetodebuglog("i","Creating lockfile.")
    else:
      writetodebuglog("i","Removing lockfile.")
      os.remove(lockfile)
  except:
    writetodebuglog("w","Cannot create/remove" + lockfile + "!")

# write data to log with timestamp
def writelog(temperature,humidity,inputs,outputs):
  dt=(strftime("%Y-%m-%d,%H:%M", gmtime()))
  lckfile(1)
  writetodebuglog("i","Writing data to log.")
  if not os.path.isfile(logfile):
    f=open(logfile,'w')
    f.close()
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
    writetodebuglog("e","Cannot write " + logfile + "!")
  lckfile(0)

# initializing ports
def initports():
  writetodebuglog("i","Initializing GPIO ports.")
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

# check external control files
def extcont(channel,status):
  writetodebuglog("i","Checking override file: "+dir_var+"out"+str(channel)+".")
  if os.path.isfile(dir_var+"out"+str(channel)):
    try:
      f=open(dir_var+"out"+str(channel),'r')
      v=f.read()
      f.close()
      if v == "neutral": s=status
      if v == "off": s="0"
      if v == "on": s="1"
    except:
      s=status
  else:
    s=status
  return s

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
      writetodebuglog("i","Meausuring T/RH.")
      shum,stemp=Adafruit_DHT.read_retry(sensor,prt_sens)
      writetodebuglog("i","Measure is done.")
      humidity=int(shum)
      temperature=int(stemp)
      blinkactled()
      if humidity<100:
        wrongvalues=0
      else:
        writetodebuglog("w","Measured values are bad!")
        wrongvalues=1
      # read input data from GPIO
      writetodebuglog("i","Reading input ports.")
      inputs=str(int(not GPIO.input(prt_in1)))
      inputs=inputs + str(int(not GPIO.input(prt_in2)))
      inputs=inputs + str(int(not GPIO.input(prt_in3)))
      inputs=inputs + str(int(not GPIO.input(prt_in4)))
      blinkactled()
      # run user's function
      writetodebuglog("i","Running function of user.")
      outputs=CR.control(temperature,humidity,inputs,wrongvalues)
      aop1=CR.autooffport1()
      blinkactled()
      # override state of outputs
      ss=""
      writetodebuglog("i","Original value of outputs: "+outputs)
      for x in range(0, 4):
        ss=ss+extcont(x+1,outputs[x])
      outputs=ss+outputs[4]+outputs[5]+outputs[6]+outputs[7]
      writetodebuglog("i","New value of outputs: "+outputs)
      # write output data to GPIO
      writetodebuglog("i","Writing output ports.")
      GPIO.output(prt_err1,not int(outputs[4]))
      GPIO.output(prt_err2,not int(outputs[5]))
      GPIO.output(prt_err3,not int(outputs[6]))
      GPIO.output(prt_err4,not int(outputs[7]))
      GPIO.output(prt_out1,not int(outputs[0]))
      GPIO.output(prt_out2,not int(outputs[1]))
      GPIO.output(prt_out3,not int(outputs[2]))
      GPIO.output(prt_out4,not int(outputs[3]))
      # auto-off first port
      if aop1 != "0":
        for i in range(int(aop1)):
          blinkactled()
        GPIO.output(prt_out1,1)
        writetodebuglog("i","Auto off enabled at first output port.")
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
      writetodebuglog("i","Waiting 10 s.")
      time.sleep(10)
  except KeyboardInterrupt:
    GPIO.cleanup
exit(0)
