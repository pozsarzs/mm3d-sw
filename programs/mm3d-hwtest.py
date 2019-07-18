#!/usr/bin/python
# +----------------------------------------------------------------------------+
# | MM3D v0.11 * Growing house controlling and remote monitoring system        |
# | Copyright (C) 2018-2019 Pozsar Zsolt <pozsar.zsolt@.szerafingomba.hu>      |
# | mm3d-hwtest.py                                                             |
# | Hardware test program                                                      |
# +----------------------------------------------------------------------------+
#
#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

import RPi.GPIO as GPIO
import Adafruit_DHT
import time

def blink_act():
    GPIO.output(24,1)
    time.sleep(0.5)
    GPIO.output(24,0)
    time.sleep(0.5)

print "\nMM3D hardware test * (C)2018-2019 Pozsar Zsolt"
print "------------------------------------------------"
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN,pull_up_down=GPIO.PUD_OFF)    # IN #1
GPIO.setup(3,GPIO.IN,pull_up_down=GPIO.PUD_OFF)    # IN #2
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_OFF)    # IN #3
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_OFF)   # IN #4
GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_OFF)   # DHT22
GPIO.setup(27,GPIO.OUT,initial=1)                  # OUT #1
GPIO.setup(22,GPIO.OUT,initial=1)                  # OUT #2
GPIO.setup(10,GPIO.OUT,initial=1)                  # OUT #3
GPIO.setup( 9,GPIO.OUT,initial=1)                  # OUT #4
GPIO.setup(14,GPIO.OUT,initial=1)                  # ERR #1 LED
GPIO.setup(15,GPIO.OUT,initial=1)                  # ERR #2 LED
GPIO.setup(18,GPIO.OUT,initial=1)                  # ERR #3 LED
GPIO.setup(23,GPIO.OUT,initial=1)                  # ERR #4 LED
GPIO.setup(24,GPIO.OUT,initial=0)                  # ACT LED

print "3/1: Read inputs (Press ^C to next!)"
try:
    while True:
        print " ",GPIO.input(2),GPIO.input(3),GPIO.input(4),GPIO.input(17)
        blink_act()
except KeyboardInterrupt:
    print ""

print "3/2: Write outputs (Press ^C to next!)"
try:
    while True:
        GPIO.output(14,0)
        blink_act()
        GPIO.output(14,1)
        GPIO.output(15,0)
        blink_act()
        GPIO.output(15,1)
        GPIO.output(18,0)
        blink_act()
        GPIO.output(18,1)
        GPIO.output(23,0)
        blink_act()
        GPIO.output(23,1)
        GPIO.output(27,0)
        blink_act()
        GPIO.output(27,1)
        GPIO.output(22,0)
        blink_act()
        GPIO.output(22,1)
        GPIO.output(10,0)
        blink_act()
        GPIO.output(10,1)
        GPIO.output(9,0)
        blink_act()
        GPIO.output(9,1)
except KeyboardInterrupt:
    GPIO.output(9,1)
    GPIO.output(10,1)
    GPIO.output(14,1)
    GPIO.output(15,1)
    GPIO.output(18,1)
    GPIO.output(22,1)
    GPIO.output(23,1)
    GPIO.output(24,0)
    GPIO.output(27,1)
    print""

print "3/3: Read DHT22 sensor (Press ^C to exit!)"
try:
    while True:
        blink_act()
        hum,temp=Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,11)
        hi=int(hum)
        ti=int(temp)
        print str(hi),"% -",str(ti),"C"
        blink_act()
        blink_act()
        blink_act()
        blink_act()
except KeyboardInterrupt:
    GPIO.cleanup()
