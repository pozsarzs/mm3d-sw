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
  global hhumidity_min
  global hhumidifier_on
  global hhumidifier_off
  global hhumidity_max
  global hhumidifier_disable_00
  global hhumidifier_disable_01
  global hhumidifier_disable_02
  global hhumidifier_disable_03
  global hhumidifier_disable_04
  global hhumidifier_disable_05
  global hhumidifier_disable_06
  global hhumidifier_disable_07
  global hhumidifier_disable_08
  global hhumidifier_disable_09
  global hhumidifier_disable_10
  global hhumidifier_disable_11
  global hhumidifier_disable_12
  global hhumidifier_disable_13
  global hhumidifier_disable_14
  global hhumidifier_disable_15
  global hhumidifier_disable_16
  global hhumidifier_disable_17
  global hhumidifier_disable_18
  global hhumidifier_disable_19
  global hhumidifier_disable_20
  global hhumidifier_disable_21
  global hhumidifier_disable_22
  global hhumidifier_disable_23
  global htemperature_min
  global hheater_on
  global hheater_off
  global htemperature_max
  global hheater_disable_00
  global hheater_disable_01
  global hheater_disable_02
  global hheater_disable_03
  global hheater_disable_04
  global hheater_disable_05
  global hheater_disable_06
  global hheater_disable_07
  global hheater_disable_08
  global hheater_disable_09
  global hheater_disable_10
  global hheater_disable_11
  global hheater_disable_12
  global hheater_disable_13
  global hheater_disable_14
  global hheater_disable_15
  global hheater_disable_16
  global hheater_disable_17
  global hheater_disable_18
  global hheater_disable_19
  global hheater_disable_20
  global hheater_disable_21
  global hheater_disable_22
  global hheater_disable_23
  global hlight_on1
  global hlight_off1
  global hlight_on2
  global hlight_off2
  global hvent_on
  global hvent_off
  global hvent_disable_00
  global hvent_disable_01
  global hvent_disable_02
  global hvent_disable_03
  global hvent_disable_04
  global hvent_disable_05
  global hvent_disable_06
  global hvent_disable_07
  global hvent_disable_08
  global hvent_disable_09
  global hvent_disable_10
  global hvent_disable_11
  global hvent_disable_12
  global hvent_disable_13
  global hvent_disable_14
  global hvent_disable_15
  global hvent_disable_16
  global hvent_disable_17
  global hvent_disable_18
  global hvent_disable_19
  global hvent_disable_20
  global hvent_disable_21
  global hvent_disable_22
  global hvent_disable_23
  global hvent_disablelowtemp_00
  global hvent_disablelowtemp_01
  global hvent_disablelowtemp_02
  global hvent_disablelowtemp_03
  global hvent_disablelowtemp_04
  global hvent_disablelowtemp_05
  global hvent_disablelowtemp_06
  global hvent_disablelowtemp_07
  global hvent_disablelowtemp_08
  global hvent_disablelowtemp_09
  global hvent_disablelowtemp_10
  global hvent_disablelowtemp_11
  global hvent_disablelowtemp_12
  global hvent_disablelowtemp_13
  global hvent_disablelowtemp_14
  global hvent_disablelowtemp_15
  global hvent_disablelowtemp_16
  global hvent_disablelowtemp_17
  global hvent_disablelowtemp_18
  global hvent_disablelowtemp_19
  global hvent_disablelowtemp_20
  global hvent_disablelowtemp_21
  global hvent_disablelowtemp_22
  global hvent_disablelowtemp_23
  global hvent_lowtemp
  global mhumidity_min
  global mhumidifier_on
  global mhumidifier_off
  global mhumidity_max
  global mhumidifier_disable_00
  global mhumidifier_disable_01
  global mhumidifier_disable_02
  global mhumidifier_disable_03
  global mhumidifier_disable_04
  global mhumidifier_disable_05
  global mhumidifier_disable_06
  global mhumidifier_disable_07
  global mhumidifier_disable_08
  global mhumidifier_disable_09
  global mhumidifier_disable_10
  global mhumidifier_disable_11
  global mhumidifier_disable_12
  global mhumidifier_disable_13
  global mhumidifier_disable_14
  global mhumidifier_disable_15
  global mhumidifier_disable_16
  global mhumidifier_disable_17
  global mhumidifier_disable_18
  global mhumidifier_disable_19
  global mhumidifier_disable_20
  global mhumidifier_disable_21
  global mhumidifier_disable_22
  global mhumidifier_disable_23
  global mtemperature_min
  global mheater_on
  global mheater_off
  global mtemperature_max
  global mheater_disable_00
  global mheater_disable_01
  global mheater_disable_02
  global mheater_disable_03
  global mheater_disable_04
  global mheater_disable_05
  global mheater_disable_06
  global mheater_disable_07
  global mheater_disable_08
  global mheater_disable_09
  global mheater_disable_10
  global mheater_disable_11
  global mheater_disable_12
  global mheater_disable_13
  global mheater_disable_14
  global mheater_disable_15
  global mheater_disable_16
  global mheater_disable_17
  global mheater_disable_18
  global mheater_disable_19
  global mheater_disable_20
  global mheater_disable_21
  global mheater_disable_22
  global mheater_disable_23
  global mlight_on1
  global mlight_off1
  global mlight_on2
  global mlight_off2
  global mvent_on
  global mvent_off
  global mvent_disable_00
  global mvent_disable_01
  global mvent_disable_02
  global mvent_disable_03
  global mvent_disable_04
  global mvent_disable_05
  global mvent_disable_06
  global mvent_disable_07
  global mvent_disable_08
  global mvent_disable_09
  global mvent_disable_10
  global mvent_disable_11
  global mvent_disable_12
  global mvent_disable_13
  global mvent_disable_14
  global mvent_disable_15
  global mvent_disable_16
  global mvent_disable_17
  global mvent_disable_18
  global mvent_disable_19
  global mvent_disable_20
  global mvent_disable_21
  global mvent_disable_22
  global mvent_disable_23
  global mvent_disablelowtemp_00
  global mvent_disablelowtemp_01
  global mvent_disablelowtemp_02
  global mvent_disablelowtemp_03
  global mvent_disablelowtemp_04
  global mvent_disablelowtemp_05
  global mvent_disablelowtemp_06
  global mvent_disablelowtemp_07
  global mvent_disablelowtemp_08
  global mvent_disablelowtemp_09
  global mvent_disablelowtemp_10
  global mvent_disablelowtemp_11
  global mvent_disablelowtemp_12
  global mvent_disablelowtemp_13
  global mvent_disablelowtemp_14
  global mvent_disablelowtemp_15
  global mvent_disablelowtemp_16
  global mvent_disablelowtemp_17
  global mvent_disablelowtemp_18
  global mvent_disablelowtemp_19
  global mvent_disablelowtemp_20
  global mvent_disablelowtemp_21
  global mvent_disablelowtemp_22
  global mvent_disablelowtemp_23
  global mvent_lowtemp
  try:
    with open(conffile) as f:
      sample_config=f.read()
    config=ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))
    hhumidity_min=int(config.get('hyphae','humidity_min'))
    hhumidifier_on=int(config.get('hyphae','humidifier_on'))
    hhumidifier_off=int(config.get('hyphae','humidifier_off'))
    hhumidity_max=int(config.get('hyphae','humidity_max'))
    hhumidifier_disable_00=int(config.get('hyphae','humidifier_disable_00'))
    hhumidifier_disable_01=int(config.get('hyphae','humidifier_disable_01'))
    hhumidifier_disable_02=int(config.get('hyphae','humidifier_disable_02'))
    hhumidifier_disable_03=int(config.get('hyphae','humidifier_disable_03'))
    hhumidifier_disable_04=int(config.get('hyphae','humidifier_disable_04'))
    hhumidifier_disable_05=int(config.get('hyphae','humidifier_disable_05'))
    hhumidifier_disable_06=int(config.get('hyphae','humidifier_disable_06'))
    hhumidifier_disable_07=int(config.get('hyphae','humidifier_disable_07'))
    hhumidifier_disable_08=int(config.get('hyphae','humidifier_disable_08'))
    hhumidifier_disable_09=int(config.get('hyphae','humidifier_disable_09'))
    hhumidifier_disable_10=int(config.get('hyphae','humidifier_disable_10'))
    hhumidifier_disable_11=int(config.get('hyphae','humidifier_disable_11'))
    hhumidifier_disable_12=int(config.get('hyphae','humidifier_disable_12'))
    hhumidifier_disable_13=int(config.get('hyphae','humidifier_disable_13'))
    hhumidifier_disable_14=int(config.get('hyphae','humidifier_disable_14'))
    hhumidifier_disable_15=int(config.get('hyphae','humidifier_disable_15'))
    hhumidifier_disable_16=int(config.get('hyphae','humidifier_disable_16'))
    hhumidifier_disable_17=int(config.get('hyphae','humidifier_disable_17'))
    hhumidifier_disable_18=int(config.get('hyphae','humidifier_disable_18'))
    hhumidifier_disable_19=int(config.get('hyphae','humidifier_disable_19'))
    hhumidifier_disable_20=int(config.get('hyphae','humidifier_disable_20'))
    hhumidifier_disable_21=int(config.get('hyphae','humidifier_disable_21'))
    hhumidifier_disable_22=int(config.get('hyphae','humidifier_disable_22'))
    hhumidifier_disable_23=int(config.get('hyphae','humidifier_disable_23'))
    htemperature_min=int(config.get('hyphae','temperature_min'))
    hheater_on=int(config.get('hyphae','heater_on'))
    hheater_off=int(config.get('hyphae','heater_off'))
    htemperature_max=int(config.get('hyphae','temperature_max'))
    hheater_disable_00=int(config.get('hyphae','heater_disable_00'))
    hheater_disable_01=int(config.get('hyphae','heater_disable_01'))
    hheater_disable_02=int(config.get('hyphae','heater_disable_02'))
    hheater_disable_03=int(config.get('hyphae','heater_disable_03'))
    hheater_disable_04=int(config.get('hyphae','heater_disable_04'))
    hheater_disable_05=int(config.get('hyphae','heater_disable_05'))
    hheater_disable_06=int(config.get('hyphae','heater_disable_06'))
    hheater_disable_07=int(config.get('hyphae','heater_disable_07'))
    hheater_disable_08=int(config.get('hyphae','heater_disable_08'))
    hheater_disable_09=int(config.get('hyphae','heater_disable_09'))
    hheater_disable_10=int(config.get('hyphae','heater_disable_10'))
    hheater_disable_11=int(config.get('hyphae','heater_disable_11'))
    hheater_disable_12=int(config.get('hyphae','heater_disable_12'))
    hheater_disable_13=int(config.get('hyphae','heater_disable_13'))
    hheater_disable_14=int(config.get('hyphae','heater_disable_14'))
    hheater_disable_15=int(config.get('hyphae','heater_disable_15'))
    hheater_disable_16=int(config.get('hyphae','heater_disable_16'))
    hheater_disable_17=int(config.get('hyphae','heater_disable_17'))
    hheater_disable_18=int(config.get('hyphae','heater_disable_18'))
    hheater_disable_19=int(config.get('hyphae','heater_disable_19'))
    hheater_disable_20=int(config.get('hyphae','heater_disable_20'))
    hheater_disable_21=int(config.get('hyphae','heater_disable_21'))
    hheater_disable_22=int(config.get('hyphae','heater_disable_22'))
    hheater_disable_23=int(config.get('hyphae','heater_disable_23'))
    hlight_on1=int(config.get('hyphae','hlight_on1'))
    hlight_off1=int(config.get('hyphae','hlight_off1'))
    hlight_on2=int(config.get('hyphae','hlight_on2'))
    hlight_off2=int(config.get('hyphae','hlight_off2'))
    hvent_on=int(config.get('hyphae','vent_on'))
    hvent_off=int(config.get('hyphae','vent_off'))
    hvent_disable_00=int(config.get('hyphae','vent_disable_03'))
    hvent_disable_01=int(config.get('hyphae','vent_disable_01'))
    hvent_disable_02=int(config.get('hyphae','vent_disable_02'))
    hvent_disable_03=int(config.get('hyphae','vent_disable_03'))
    hvent_disable_04=int(config.get('hyphae','vent_disable_04'))
    hvent_disable_05=int(config.get('hyphae','vent_disable_05'))
    hvent_disable_06=int(config.get('hyphae','vent_disable_06'))
    hvent_disable_07=int(config.get('hyphae','vent_disable_07'))
    hvent_disable_08=int(config.get('hyphae','vent_disable_08'))
    hvent_disable_09=int(config.get('hyphae','vent_disable_09'))
    hvent_disable_10=int(config.get('hyphae','vent_disable_10'))
    hvent_disable_11=int(config.get('hyphae','vent_disable_11'))
    hvent_disable_12=int(config.get('hyphae','vent_disable_12'))
    hvent_disable_13=int(config.get('hyphae','vent_disable_13'))
    hvent_disable_14=int(config.get('hyphae','vent_disable_14'))
    hvent_disable_15=int(config.get('hyphae','vent_disable_15'))
    hvent_disable_16=int(config.get('hyphae','vent_disable_16'))
    hvent_disable_17=int(config.get('hyphae','vent_disable_17'))
    hvent_disable_18=int(config.get('hyphae','vent_disable_18'))
    hvent_disable_19=int(config.get('hyphae','vent_disable_19'))
    hvent_disable_20=int(config.get('hyphae','vent_disable_20'))
    hvent_disable_21=int(config.get('hyphae','vent_disable_21'))
    hvent_disable_22=int(config.get('hyphae','vent_disable_22'))
    hvent_disable_23=int(config.get('hyphae','vent_disable_23'))
    hvent_disablelowtemp_00=int(config.get('hyphae','vent_disablelowtemp_00'))
    hvent_disablelowtemp_01=int(config.get('hyphae','vent_disablelowtemp_01'))
    hvent_disablelowtemp_02=int(config.get('hyphae','vent_disablelowtemp_02'))
    hvent_disablelowtemp_03=int(config.get('hyphae','vent_disablelowtemp_03'))
    hvent_disablelowtemp_04=int(config.get('hyphae','vent_disablelowtemp_04'))
    hvent_disablelowtemp_05=int(config.get('hyphae','vent_disablelowtemp_05'))
    hvent_disablelowtemp_06=int(config.get('hyphae','vent_disablelowtemp_06'))
    hvent_disablelowtemp_07=int(config.get('hyphae','vent_disablelowtemp_07'))
    hvent_disablelowtemp_08=int(config.get('hyphae','vent_disablelowtemp_08'))
    hvent_disablelowtemp_09=int(config.get('hyphae','vent_disablelowtemp_09'))
    hvent_disablelowtemp_10=int(config.get('hyphae','vent_disablelowtemp_10'))
    hvent_disablelowtemp_11=int(config.get('hyphae','vent_disablelowtemp_11'))
    hvent_disablelowtemp_12=int(config.get('hyphae','vent_disablelowtemp_12'))
    hvent_disablelowtemp_13=int(config.get('hyphae','vent_disablelowtemp_13'))
    hvent_disablelowtemp_14=int(config.get('hyphae','vent_disablelowtemp_14'))
    hvent_disablelowtemp_15=int(config.get('hyphae','vent_disablelowtemp_15'))
    hvent_disablelowtemp_16=int(config.get('hyphae','vent_disablelowtemp_16'))
    hvent_disablelowtemp_17=int(config.get('hyphae','vent_disablelowtemp_17'))
    hvent_disablelowtemp_18=int(config.get('hyphae','vent_disablelowtemp_18'))
    hvent_disablelowtemp_19=int(config.get('hyphae','vent_disablelowtemp_19'))
    hvent_disablelowtemp_20=int(config.get('hyphae','vent_disablelowtemp_20'))
    hvent_disablelowtemp_21=int(config.get('hyphae','vent_disablelowtemp_21'))
    hvent_disablelowtemp_22=int(config.get('hyphae','vent_disablelowtemp_22'))
    hvent_disablelowtemp_23=int(config.get('hyphae','vent_disablelowtemp_23'))
    hvent_lowtemp=int(config.get('hyphae','vent_lowtemp'))
    mhumidity_min=int(config.get('mushroom','humidity_min'))
    mhumidifier_on=int(config.get('mushroom','humidifier_on'))
    mhumidifier_off=int(config.get('mushroom','humidifier_off'))
    mhumidity_max=int(config.get('mushroom','humidity_max'))
    mhumidifier_disable_00=int(config.get('mushroom','humidifier_disable_00'))
    mhumidifier_disable_01=int(config.get('mushroom','humidifier_disable_01'))
    mhumidifier_disable_02=int(config.get('mushroom','humidifier_disable_02'))
    mhumidifier_disable_03=int(config.get('mushroom','humidifier_disable_03'))
    mhumidifier_disable_04=int(config.get('mushroom','humidifier_disable_04'))
    mhumidifier_disable_05=int(config.get('mushroom','humidifier_disable_05'))
    mhumidifier_disable_06=int(config.get('mushroom','humidifier_disable_06'))
    mhumidifier_disable_07=int(config.get('mushroom','humidifier_disable_07'))
    mhumidifier_disable_08=int(config.get('mushroom','humidifier_disable_08'))
    mhumidifier_disable_09=int(config.get('mushroom','humidifier_disable_09'))
    mhumidifier_disable_10=int(config.get('mushroom','humidifier_disable_10'))
    mhumidifier_disable_11=int(config.get('mushroom','humidifier_disable_11'))
    mhumidifier_disable_12=int(config.get('mushroom','humidifier_disable_12'))
    mhumidifier_disable_13=int(config.get('mushroom','humidifier_disable_13'))
    mhumidifier_disable_14=int(config.get('mushroom','humidifier_disable_14'))
    mhumidifier_disable_15=int(config.get('mushroom','humidifier_disable_15'))
    mhumidifier_disable_16=int(config.get('mushroom','humidifier_disable_16'))
    mhumidifier_disable_17=int(config.get('mushroom','humidifier_disable_17'))
    mhumidifier_disable_18=int(config.get('mushroom','humidifier_disable_18'))
    mhumidifier_disable_19=int(config.get('mushroom','humidifier_disable_19'))
    mhumidifier_disable_20=int(config.get('mushroom','humidifier_disable_20'))
    mhumidifier_disable_21=int(config.get('mushroom','humidifier_disable_21'))
    mhumidifier_disable_22=int(config.get('mushroom','humidifier_disable_22'))
    mhumidifier_disable_23=int(config.get('mushroom','humidifier_disable_23'))
    mtemperature_min=int(config.get('mushroom','temperature_min'))
    mheater_on=int(config.get('mushroom','heater_on'))
    mheater_off=int(config.get('mushroom','heater_off'))
    mtemperature_max=int(config.get('mushroom','temperature_max'))
    mheater_disable_00=int(config.get('mushroom','heater_disable_00'))
    mheater_disable_01=int(config.get('mushroom','heater_disable_01'))
    mheater_disable_02=int(config.get('mushroom','heater_disable_02'))
    mheater_disable_03=int(config.get('mushroom','heater_disable_03'))
    mheater_disable_04=int(config.get('mushroom','heater_disable_04'))
    mheater_disable_05=int(config.get('mushroom','heater_disable_05'))
    mheater_disable_06=int(config.get('mushroom','heater_disable_06'))
    mheater_disable_07=int(config.get('mushroom','heater_disable_07'))
    mheater_disable_08=int(config.get('mushroom','heater_disable_08'))
    mheater_disable_09=int(config.get('mushroom','heater_disable_09'))
    mheater_disable_10=int(config.get('mushroom','heater_disable_10'))
    mheater_disable_11=int(config.get('mushroom','heater_disable_11'))
    mheater_disable_12=int(config.get('mushroom','heater_disable_12'))
    mheater_disable_13=int(config.get('mushroom','heater_disable_13'))
    mheater_disable_14=int(config.get('mushroom','heater_disable_14'))
    mheater_disable_15=int(config.get('mushroom','heater_disable_15'))
    mheater_disable_16=int(config.get('mushroom','heater_disable_16'))
    mheater_disable_17=int(config.get('mushroom','heater_disable_17'))
    mheater_disable_18=int(config.get('mushroom','heater_disable_18'))
    mheater_disable_19=int(config.get('mushroom','heater_disable_19'))
    mheater_disable_20=int(config.get('mushroom','heater_disable_20'))
    mheater_disable_21=int(config.get('mushroom','heater_disable_21'))
    mheater_disable_22=int(config.get('mushroom','heater_disable_22'))
    mheater_disable_23=int(config.get('mushroom','heater_disable_23'))
    mlight_on1=int(config.get('mushroom','hlight_on1'))
    mlight_off1=int(config.get('mushroom','hlight_off1'))
    mlight_on2=int(config.get('mushroom','hlight_on2'))
    mlight_off2=int(config.get('mushroom','hlight_off2'))
    mvent_on=int(config.get('mushroom','vent_on'))
    mvent_off=int(config.get('mushroom','vent_off'))
    mvent_disable_00=int(config.get('mushroom','vent_disable_03'))
    mvent_disable_01=int(config.get('mushroom','vent_disable_01'))
    mvent_disable_02=int(config.get('mushroom','vent_disable_02'))
    mvent_disable_03=int(config.get('mushroom','vent_disable_03'))
    mvent_disable_04=int(config.get('mushroom','vent_disable_04'))
    mvent_disable_05=int(config.get('mushroom','vent_disable_05'))
    mvent_disable_06=int(config.get('mushroom','vent_disable_06'))
    mvent_disable_07=int(config.get('mushroom','vent_disable_07'))
    mvent_disable_08=int(config.get('mushroom','vent_disable_08'))
    mvent_disable_09=int(config.get('mushroom','vent_disable_09'))
    mvent_disable_10=int(config.get('mushroom','vent_disable_10'))
    mvent_disable_11=int(config.get('mushroom','vent_disable_11'))
    mvent_disable_12=int(config.get('mushroom','vent_disable_12'))
    mvent_disable_13=int(config.get('mushroom','vent_disable_13'))
    mvent_disable_14=int(config.get('mushroom','vent_disable_14'))
    mvent_disable_15=int(config.get('mushroom','vent_disable_15'))
    mvent_disable_16=int(config.get('mushroom','vent_disable_16'))
    mvent_disable_17=int(config.get('mushroom','vent_disable_17'))
    mvent_disable_18=int(config.get('mushroom','vent_disable_18'))
    mvent_disable_19=int(config.get('mushroom','vent_disable_19'))
    mvent_disable_20=int(config.get('mushroom','vent_disable_20'))
    mvent_disable_21=int(config.get('mushroom','vent_disable_21'))
    mvent_disable_22=int(config.get('mushroom','vent_disable_22'))
    mvent_disable_23=int(config.get('mushroom','vent_disable_23'))
    mvent_disablelowtemp_00=int(config.get('mushroom','vent_disablelowtemp_00'))
    mvent_disablelowtemp_01=int(config.get('mushroom','vent_disablelowtemp_01'))
    mvent_disablelowtemp_02=int(config.get('mushroom','vent_disablelowtemp_02'))
    mvent_disablelowtemp_03=int(config.get('mushroom','vent_disablelowtemp_03'))
    mvent_disablelowtemp_04=int(config.get('mushroom','vent_disablelowtemp_04'))
    mvent_disablelowtemp_05=int(config.get('mushroom','vent_disablelowtemp_05'))
    mvent_disablelowtemp_06=int(config.get('mushroom','vent_disablelowtemp_06'))
    mvent_disablelowtemp_07=int(config.get('mushroom','vent_disablelowtemp_07'))
    mvent_disablelowtemp_08=int(config.get('mushroom','vent_disablelowtemp_08'))
    mvent_disablelowtemp_09=int(config.get('mushroom','vent_disablelowtemp_09'))
    mvent_disablelowtemp_10=int(config.get('mushroom','vent_disablelowtemp_10'))
    mvent_disablelowtemp_11=int(config.get('mushroom','vent_disablelowtemp_11'))
    mvent_disablelowtemp_12=int(config.get('mushroom','vent_disablelowtemp_12'))
    mvent_disablelowtemp_13=int(config.get('mushroom','vent_disablelowtemp_13'))
    mvent_disablelowtemp_14=int(config.get('mushroom','vent_disablelowtemp_14'))
    mvent_disablelowtemp_15=int(config.get('mushroom','vent_disablelowtemp_15'))
    mvent_disablelowtemp_16=int(config.get('mushroom','vent_disablelowtemp_16'))
    mvent_disablelowtemp_17=int(config.get('mushroom','vent_disablelowtemp_17'))
    mvent_disablelowtemp_18=int(config.get('mushroom','vent_disablelowtemp_18'))
    mvent_disablelowtemp_19=int(config.get('mushroom','vent_disablelowtemp_19'))
    mvent_disablelowtemp_20=int(config.get('mushroom','vent_disablelowtemp_20'))
    mvent_disablelowtemp_21=int(config.get('mushroom','vent_disablelowtemp_21'))
    mvent_disablelowtemp_22=int(config.get('mushroom','vent_disablelowtemp_22'))
    mvent_disablelowtemp_23=int(config.get('mushroom','vent_disablelowtemp_23'))
    mvent_lowtemp=int(config.get('mushroom','vent_lowtemp'))
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

# control function
def control(temperature,humidity,inputs,wrongvalues):
  in1=int(inputs[0])
  in2=int(inputs[1])
  in3=int(inputs[2])
  in4=int(inputs[3])

  #    humidity:  integer  measured relative humidity in %
  # temperature:  integer  measured temperature in degree Celsius
  # wrongvalues:  measured data is invalid
  #         in1:  integer  status of input port #1, 0: opened | 1: closed to GND
  #         in2:  integer  status of input port #2, 0: opened | 1: closed to GND
  #         in3:  integer  status of input port #3, 0: opened | 1: closed to GND
  #         in4:  integer  status of input port #4, 0: opened | 1: closed to GND

  # in1:  (unused)
  # in2:  water pressure (closed: good)
  # in3:  growing hyphae/mushroom (closed: hyphae)
  # in4:  (unused)
  # err1: bad relative humidity
  # err2: bad water pressure
  # err3: bad measured data
  # err4: bad temperature
  # out1: humidifying
  # out2: lighting
  # out3: ventilation
  # out4: heating

  # check water pressure:
  if in2==1:
    err2=0
  else:
    err2=1

  # lighting
  h=int(time.strftime("%H"))
  if in3==1:
    # growing hyphae
    if (h>hlight_on1) and (h<hlight_off1):
      out2=1
    else:
      out2=0
    if (h>hlight_on2) and (h<hlight_off2):
      out2=1
    else:
      out2=0
  else:
    # growing mushroom
    if (h>mlight_on1) and (h<mlight_off1):
      out2=1
    else:
      out2=0
    if (h>mlight_on2) and (h<mlight_off2):
      out2=1
    else:
      out2=0

# <-- Idaig kesz!

  # check growing mode:
  if in3==1:
    # growing hyphae
    humidity_min=65
    humidity_max=70
    temperature_min=17
    temperature_max=25
    light_on=0
    light_off=0
    vent_on=0
    vent_off=0
  else:
    # growing mushroom
    humidity_min=70
    humidity_max=85
    temperature_min=7
    temperature_max=25
    light_on=14
    light_off=22
    vent_on=0
    vent_off=30
  allowed_hour=14
  allowed_minute=0

  # humidifying
  if (wrongvalues == 0) and ((humidity<humidity_min) or (humidity>humidity_max)):
    err1=1
  else:
    err1=0

  if (wrongvalues == 0) and ((humidity<humidity_min) and (err2==0)):
    h=int(time.strftime("%H"))
    m=int(time.strftime("%M"))
    if (h==allowed_hour) and (m==allowed_minute):
      out1=1
    else:
      out1=0
  else:
    out1=0

  # ventilation
  m=int(time.strftime("%M"))
  if (m>vent_on) and (m<vent_off):
    out3=1
  else:
    out3=0

  # heating
  if (wrongvalues == 0) and ((temperature<temperature_min) or (temperature>temperature_max)):
    err4=1
  else:
    err4=0

  if (wrongvalues == 0) and (temperature<temperature_min):
    out4=1
  else:
    out4=0

# <-- Innentol kesz!

  # other error light
  err3=wrongvalues

  # out1:  integer  status of output port #1, 0: switch off | 1: switch on relay
  # out2:  integer  status of output port #2, 0: switch off | 1: switch on relay
  # out3:  integer  status of output port #3, 0: switch off | 1: switch on relay
  # out4:  integer  status of output port #4, 0: switch off | 1: switch on relay
  # err1:  integer  status of error light #1, 0: switch off | 1: switch on LED
  # err2:  integer  status of error light #2, 0: switch off | 1: switch on LED
  # err3:  integer  status of error light #3, 0: switch off | 1: switch on LED
  # err4:  integer  status of error light #4, 0: switch off | 1: switch on LED

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
