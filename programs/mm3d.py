#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.4 * Growing house controlling and remote monitoring system         |
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
import array as arr
import daemon
import io
import os
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import gmtime, strftime

# write a line to debug logfile
def writetodebuglog(level,text):
  if dbg_log=="1":
    if level=="i":
      lv="INFO   "
    if level=="w":
      lv="WARNING"
    if level=="e":
      lv="ERROR  "
    debugfile=dir_log+time.strftime("debug-%Y%m%d.log")
    dt=(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    try:
      with open(debugfile, "a") as d:
        d.write(dt+'  '+lv+' '+text+'\n')
        d.close()
    except:
      print ""

# create and remove lock file
def lckfile(mode):
  try:
    if mode>0:
      lcf=open(lockfile,'w')
      lcf.close()
      writetodebuglog(dir_log,"i","Creating lockfile.")
    else:
      writetodebuglog("i","Removing lockfile.")
      os.remove(lockfile)
  except:
    writetodebuglog("w","Cannot create/remove"+lockfile+"!")

# write data to log with timestamp
def writelog(temperature,humidity,inputs,outputs):
  dt=(strftime("%Y-%m-%d,%H:%M", gmtime()))
  lckfile(1)
  writetodebuglog("i","Writing data to log.")
  if not os.path.isfile(logfile):
    f=open(logfile,'w')
    f.close()
  try:
    with open(logfile,"r+") as f:
      first_line=f.readline()
      lines=f.readlines()
      f.seek(0)
      f.write(dt+','+str(temperature)+','+str(humidity)+','+
              inputs[0]+','+inputs[1]+','+inputs[2]+','+inputs[3]+','+
              outputs[0]+','+outputs[1]+','+outputs[2]+','+outputs[3]+','+
              outputs[4]+','+outputs[5]+','+outputs[6]+','+outputs[7]+'\n')
      f.write(first_line)
      f.writelines(lines)
      f.close()
  except:
    writetodebuglog("e","Cannot write "+logfile+"!")
  lckfile(0)

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
      sample_config=f.read()
    config=ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    dbg_log='0'
    dbg_log=config.get('others','dbg_log')
    dir_log=config.get('directories','dir_log')
    dir_var=config.get('directories','dir_var')
    logfile=dir_log+'mm3d.log'
    lockfile=config.get('directories','dir_lck')+'mm3d.lck'
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
    writetodebuglog("e","Cannot open "+conffile+"!")

# load environment characteristics
def loadenvirchars(conffile):
  global hheater_disable=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global hheater_off
  global hheater_on
  global hhumidifier_disable=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global hhumidifier_off
  global hhumidifier_on
  global hhumidity_max
  global hhumidity_min
  global hlight_off1
  global hlight_off2
  global hlight_on1
  global hlight_on2
  global htemperature_max
  global htemperature_min
  global hvent_disable=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global hvent_disablelowtemp=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global hvent_lowtemp
  global hvent_off
  global hvent_on
  global mheater_disable=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global mheater_off
  global mheater_on
  global mhumidifier_disable=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global mhumidifier_off
  global mhumidifier_on
  global mhumidity_max
  global mhumidity_min
  global mlight_off1
  global mlight_off2
  global mlight_on1
  global mlight_on2
  global mtemperature_max
  global mtemperature_min
  global mvent_disable=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global mvent_disablelowtemp=arr.array('i',[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,])
  global mvent_lowtemp
  global mvent_off
  global mvent_on
  try:
    with open(conffile) as f:
      sample_config=f.read()
    config=ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    for x in range(24):
      hhumidifier_disable[x]=int(config.get('hyphae','humidifier_disable_'+str(x)))
    for x in range(24):
      hheater_disable[x]=int(config.get('hyphae','heater_disable_'+str(x)))
    for x in range(24):
      hvent_disable[x]=int(config.get('hyphae','vent_disable_'+str(x)))
    for x in range(24):
      hvent_disablelowtemp[x]=int(config.get('hyphae','vent_disablelowtemp_'+str(x)))
    hheater_off=int(config.get('hyphae','heater_off'))
    hheater_on=int(config.get('hyphae','heater_on'))
    hhumidifier_off=int(config.get('hyphae','humidifier_off'))
    hhumidifier_on=int(config.get('hyphae','humidifier_on'))
    hhumidity_max=int(config.get('hyphae','humidity_max'))
    hhumidity_min=int(config.get('hyphae','humidity_min'))
    hlight_off1=int(config.get('hyphae','light_off1'))
    hlight_off2=int(config.get('hyphae','light_off2'))
    hlight_on1=int(config.get('hyphae','light_on1'))
    hlight_on2=int(config.get('hyphae','light_on2'))
    htemperature_max=int(config.get('hyphae','temperature_max'))
    htemperature_min=int(config.get('hyphae','temperature_min'))
    hvent_lowtemp=int(config.get('hyphae','vent_lowtemp'))
    hvent_off=int(config.get('hyphae','vent_off'))
    hvent_on=int(config.get('hyphae','vent_on'))
    for x in range(24):
      mhumidifier_disable[x]=int(config.get('mushroom','humidifier_disable_'+str(x)))
    for x in range(24):
      mheater_disable[x]=int(config.get('mushroom','heater_disable_'+str(x)))
    for x in range(24):
      mvent_disable[x]=int(config.get('mushroom','vent_disable_'+str(x)))
    for x in range(24):
      mvent_disablelowtemp[x]=int(config.get('mushroom','vent_disablelowtemp_'+str(x)))
    mheater_off=int(config.get('mushroom','heater_off'))
    mheater_on=int(config.get('mushroom','heater_on'))
    mhumidifier_off=int(config.get('mushroom','humidifier_off'))
    mhumidifier_on=int(config.get('mushroom','humidifier_on'))
    mhumidity_max=int(config.get('mushroom','humidity_max'))
    mhumidity_min=int(config.get('mushroom','humidity_min'))
    mlight_off1=int(config.get('mushroom','light_off1'))
    mlight_off2=int(config.get('mushroom','light_off2'))
    mlight_on1=int(config.get('mushroom','light_on1'))
    mlight_on2=int(config.get('mushroom','light_on2'))
    mtemperature_max=int(config.get('mushroom','temperature_max'))
    mtemperature_min=int(config.get('mushroom','temperature_min'))
    mvent_lowtemp=int(config.get('mushroom','vent_lowtemp'))
    mvent_off=int(config.get('mushroom','vent_off'))
    mvent_on=int(config.get('mushroom','vent_on'))
    writetodebuglog("i","Environment characteristics is loaded.")
  except:
    writetodebuglog("e","Cannot open "+conffile+"!")

# write data to log with timestamp
def writelog(temperature,humidity,inputs,outputs):
  dt=(strftime("%Y-%m-%d,%H:%M",gmtime()))
  lckfile(1)
  writetodebuglog("i","Writing data to log.")
  if not os.path.isfile(logfile):
    f=open(logfile,'w')
    f.close()
  try:
    with open(logfile,"r+") as f:
      first_line=f.readline()
      lines=f.readlines()
      f.seek(0)
      f.write(dt+','+str(temperature)+','+str(humidity)+','+
              inputs[0]+','+inputs[1]+','+inputs[2]+','+inputs[3]+','+
              outputs[0]+','+outputs[1]+','+outputs[2]+','+outputs[3]+','+
              outputs[4]+','+outputs[5]+','+outputs[6]+','+outputs[7]+'\n')
      f.write(first_line)
      f.writelines(lines)
      f.close()
  except:
    writetodebuglog("e","Cannot write "+logfile+"!")
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
  writetodebuglog(dir_log,"i","Checking override file: "+dir_var+"out"+str(channel)+".")
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

# auto off OUT #1
def autooffport1():
  # aop1:  auto off port after switch on (in s)
  aop1="5"
  return aop1

# control output ports and error lights
def control(temperature,humidity,inputs,wrongvalues):
  in1=int(inputs[0])
  in2=int(inputs[1])
  in3=int(inputs[2])
  in4=int(inputs[3])

  # input values:
  # humidity:      integer   measured relative humidity in %
  # temperature:   integer   measured temperature in degree Celsius
  # wrongvalues:   integer   measured data is invalid
  # in1-4:         integer   status of input ports #1-4 (1: closed to GND)

  h=int(time.strftime("%H"))
  m=int(time.strftime("%M"))

  # !!! ami meg kell bele:
  # !!!   - kulso homerseklet adat lekerese --> exttemp
  exttemp=0

  # check water pressure:
  # in2:  water pressure input (closed: good)
  # err2: bad water pressure error light
  err2=0 if in2==1 else 1

  # switch on-off lamps
  # in3:  change growing mode input (closed: hyphae)
  # out2: lighting output
  if in3==1:
    # growing hyphae
    out2=1 if (h=>hlight_on1) or (h=>hlight_on2) else 0
    out2=0 if (h=>hlight_off1) or (h=>hlight_off2)
  else:
    # growing mushroom
    out2=1 if (h=>mlight_on1) or (h=>mlight_on2) else 0
    out2=0 if (h=>mlight_off1) or (h=>mlight_off2)

  # switch on-off ventilators
  # in3:  change growing mode input (closed: hyphae)
  # out3: ventilating output
  if in3==1:
    # growing hyphae
    if (m>hvent_on) and (m<hvent_off):
      out3=1
      out3=0 if hvent_disable[h]==1
      out3=0 if (hvent_disablelowtemp[h]==1) and (exttemp<=hvent_lowtemp)
    else:
      out3=0
  else:
    # growing mushroom
    if (m>mvent_on) and (m<mvent_off):
      out3=1
      out3=0 if mvent_disable[h]==1
      out3=0 if (mvent_disablelowtemp[h]==1) and (exttemp<=mvent_lowtemp)
    else:
      out3=0

  # switch on-off heaters
  # in3:  change growing mode input (closed: hyphae)
  # err4: bad temperature
  # out4: heating output
  if in3==1:
    # growing hyphae
    err4=0
    err4=1 if (wrongvalues==0) and ((temperature<htemperature_min)
    err4=1 if (wrongvalues==0) and ((temperature>htemperature_max)
    out4=0
    out4=1 if (wrongvalues==0) and ((temperature<=hheater_on)
    out4=0 if (wrongvalues==0) and ((temperature>=hheater_off)
    out4=0 if hheater_disable[h]==1
  else:
    # growing mushroom
    err4=0
    err4=1 if (wrongvalues==0) and ((temperature<mtemperature_min)
    err4=1 if (wrongvalues==0) and ((temperature>mtemperature_max)
    out4=0
    out4=1 if (wrongvalues==0) and ((temperature<=mheater_on)
    out4=0 if (wrongvalues==0) and ((temperature>=mheater_off)
    out4=0 if mheater_disable[h]==1

  # switch on-off humidifier
  # in3:  change growing mode input (closed: hyphae)
  # err1: bad relative humidity
  # out1: humidifying output
  if in3==1:
    # growing hyphae
    err1=0
    err1=1 if (wrongvalues==0) and ((humidity<hhumidity_min)
    err1=1 if (wrongvalues==0) and ((humidity>hhumidity_max)
    out1=0
    out1=1 if (wrongvalues==0) and ((humidity<=hhumidifier_on)
    out1=0 if (wrongvalues==0) and ((humidity>=hhumidifier_off)
    out1=0 if hhumidifier_disable[h]==1
  else:
    # growing mushroom
    err1=0
    err1=1 if (wrongvalues==0) and ((humidity<mhumidity_min)
    err1=1 if (wrongvalues==0) and ((humidity>mhumidity_max)
    out1=0
    out1=1 if (wrongvalues==0) and ((humidity<=mhumidifier_on)
    out1=0 if (wrongvalues==0) and ((humidity>=mhumidifier_off)
    out1=0 if mhumidifier_disable[h]==1


#  ami meg kell bele:
#  - magas paratartalomnal szelloztetes
#  - magas homersekletnel szelloztetes
#  - alacsony homersekletnel, ha kint melegebb van, akkor szelloztetes


  # other error light
  # err3: measured data is wrong
  err3=wrongvalues

  # out1-4:  integer   status of out ports #1-4, 1: switch on relay
  # err1-4:  integer   status of error lights #1-4, 1: switch on LED

  outputs=str(out1)+str(out2)+str(out3)+str(out4)+ \
          str(err1)+str(err2)+str(err3)+str(err4)
  return outputs

# main program
loadconfiguration('/usr/local/etc/mm3d/mm3d.ini')
loadenvirchars('/usr/local/etc/mm3d/envir.ini')
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
        wrongvalues=1
        writetodebuglog("w","Measured values are bad!")
      # read input data from GPIO
      writetodebuglog("i","Reading input ports.")
      inputs=str(int(not GPIO.input(prt_in1)))
      inputs=inputs+str(int(not GPIO.input(prt_in2)))
      inputs=inputs+str(int(not GPIO.input(prt_in3)))
      inputs=inputs+str(int(not GPIO.input(prt_in4)))
      blinkactled()
      # run user's function
      writetodebuglog("i","Running function of user.")
      outputs=control(temperature,humidity,inputs,wrongvalues)
      aop1=autooffport1()
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
      if aop1!="0":
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
