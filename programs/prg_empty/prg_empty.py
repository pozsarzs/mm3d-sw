#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.3 * Growing house controlling and remote monitoring system         |
# | Copyright (C) 2018-2019 Pozsar Zsolt <pozsar.zsolt@.szerafingomba.hu>      |
# | prg_empty.py                                                               |
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

  aop1="0"

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

  # Write here!

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
