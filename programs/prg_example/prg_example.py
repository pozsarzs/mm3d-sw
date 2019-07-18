#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.2 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018-2019 Pozsar Zsolt <pozsar.zsolt@.szerafingomba.hu>      |
# | prg_example.py                                                             |
# | User's program                                                             |
# +----------------------------------------------------------------------------+
#
#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

import time

def autooffport1():
  # Auto off OUT #1
  # Use this variable:
  #         aop1:  auto off OUT #1 port after switch on (in s)
  #
  # ------------------------- do not edit before this row ----------------------

  aop1="5"

  # ------------------------- do not edit after this row -----------------------
  #
  return aop1

def control(temperature,humidity,inputs,wrongvalues):
  in1=int(inputs[0])
  in2=int(inputs[1])
  in3=int(inputs[2])
  in4=int(inputs[3])
  #
  # Use thes variables:
  # ------------------
  #    humidity:  integer  measured relative humidity in %
  #         in1:  integer  status of input port #1, 0: opened | 1: closed to GND
  #         in2:  integer  status of input port #2, 0: opened | 1: closed to GND
  #         in3:  integer  status of input port #3, 0: opened | 1: closed to GND
  #         in4:  integer  status of input port #4, 0: opened | 1: closed to GND
  # temperature:  integer  measured temperature in degree Celsius
  #
  # ------------------------- do not edit before this row ----------------------

  # Growing oyster mushroom - cooperation with MM1A and MM2A analog controllers
  #
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

  enabled_hour=14
  enabled_interval=1

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

  # humidifying
  if wrongvalues == 0:
    if (humidity<humidity_min) or (humidity>humidity_max):
      err1=1
    else:
      err1=0
    if (humidity<humidity_min) and (err2==0):
      h=int(time.strftime("%H"))
      m=int(time.strftime("%M"))
      if (h==enabled_hour) and (m<=enabled_interval):
        out1=1
      else:
        out1=0
    else:
      out1=0

  # lighting
  h=int(time.strftime("%H"))
  if (h>light_on) and (h<light_off):
    out2=1
  else:
    out2=0

  # ventilation
  m=int(time.strftime("%M"))
  if (m>vent_on) and (m<vent_off):
    out3=1
  else:
    out3=0

  # heating
  if wrongvalues == 0:
    if (temperature<temperature_min) or (temperature>temperature_max):
      err4=1
    else:
      err4=0
    if (temperature<temperature_min):
      out4=1
    else:
      out4=0

  # other error light
  err3=wrongvalues

  # ------------------------- do not edit after this row -----------------------
  #
  # output data
  # -----------
  # out1:  integer  status of output port #1, 0: switch off | 1: switch on relay
  # out2:  integer  status of output port #2, 0: switch off | 1: switch on relay
  # out3:  integer  status of output port #3, 0: switch off | 1: switch on relay
  # out4:  integer  status of output port #4, 0: switch off | 1: switch on relay
  # err1:  integer  status of error light #1, 0: switch off | 1: switch on LED
  # err2:  integer  status of error light #2, 0: switch off | 1: switch on LED
  # err3:  integer  status of error light #3, 0: switch off | 1: switch on LED
  # err4:  integer  status of error light #4, 0: switch off | 1: switch on LED
  #
  outputs=str(out1)+str(out2)+str(out3)+str(out4)+ \
          str(err1)+str(err2)+str(err3)+str(err4)
  return outputs
