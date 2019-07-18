#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.1 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018 Pozsar Zsolt <pozsar.zsolt@.szerafingomba.hu>           |
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

def control(temperature,humidity,inputs):
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
  # err3: (unused)
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

  # check growing mode:
  if in3==1:
    # growing hyphae
    humidity_min=60
    humidity_max=70
    temperature_min=17
    temperature_max=23
    light_on=0
    light_off=0
    vent_on1=0
    vent_off1=0
    vent_on2=0
    vent_off2=0
  else:
    # growing mushroom
    humidity_min=70
    humidity_max=80
    temperature_min=7
    temperature_max=15
    light_on=7
    light_off=16
    vent_on1=0
    vent_off1=15
    vent_on2=30
    vent_off2=45

  # humidifying
  if (humidity<humidity_min) or (humidity>humidity_max):
    err1=1
  else:
    err1=0
  if (humidity<humidity_min) and (err2==0):
    out1=1
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
  if (m>vent_on1) and (m<vent_off1):
    out3=1
  else:
    out3=0
  if (m>vent_on2) and (m<vent_off2):
    out3=1
  else:
    out3=0

  # heating
  if (temperature<temperature_min) or (temperature>temperature_max):
    err4=1
  else:
    err4=0
  if (temperature<temperature_min):
    out4=1
  else:
    out4=0

  # unused error lights and outputs
  err3=0

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
