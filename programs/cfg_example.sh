#!/bin/bash
# +----------------------------------------------------------------------------+
# | MM3D v0.11 * Growing house controlling and remote monitoring system        |
# | Copyright (C) 2018-2019 Pozsár Zsolt <pozsar.zsolt@.szerafingomba.hu>      |
# | cfg_example.sh                                                             |
# | User's program configurator                                                |
# +----------------------------------------------------------------------------+
#
#   This program is free software: you can redistribute it and/or modify it
# under the terms of the European Union Public License 1.1 version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.

BACKTITLE="Configure and make user's controller program - cfg_example.sh v0.11"
TITLE=" Oyster mushroom "
MENU1="Minimum humidity [0-100 %]"
MENU2="Maximum humidity [0-100 %]"
MENU3="Minimum temperature [0-40 °C]"
MENU4="Maximum temperature [0-40 °C]"
MENU5="Time when light on [0-23 h]"
MENU6="Time when light off [0-23 h]"
MENU7="Time when ventilation on [0-59 m]"
MENU8="Time when ventilation off [0-59 m]"

INIFILE=./cfg_example.ini
PRGDIR=../programs
PYFILE=$PRGDIR/prg_example.py
BAKFILE=$PRGDIR/prg_example.bak

ini_parser()
{
  section=$1
  key=$2
  shift; shift
  files=$*

  for ini_file in $files
  do
    [ -f "$ini_file" ] || continue
    value=$(
    if [ -n "$section" ]; then
      sed -n "/^\[$section\]/, /^\[/p" $ini_file
    else
      cat $ini_file
    fi |
    egrep "^ *\b$key\b *=" |
    head -1 | cut -f2 -d'=' |
    sed 's/^[ "'']*//g' |
    sed 's/[ ",'']*$//g' )
    if [ -n "$value" ]; then
      echo $value
      return
    fi
  done
}

loadconfig()
{
  # default values
  HHMAX=0
  HHMIN=0
  HLOFF=0
  HLON=0
  HTMAX=0
  HTMIN=0
  HVOFF=0
  HVON=0
  MHMAX=0
  MHMIN=0
  MLOFF=0
  MLON=0
  MTMAX=0
  MTMIN=0
  MVOFF=0
  MVON=0
  # loaded values
  if [ -f $INIFILE ]
  then
    HHMAX=$(ini_parser "hyphae" "humidity_max" $INIFILE)
    HHMIN=$(ini_parser "hyphae" "humidity_min" $INIFILE)
    HLOFF=$(ini_parser "hyphae" "light_off" $INIFILE)
    HLON=$(ini_parser "hyphae" "light_on" $INIFILE)
    HTMAX=$(ini_parser "hyphae" "temperature_max" $INIFILE)
    HTMIN=$(ini_parser "hyphae" "temperature_min" $INIFILE)
    HVOFF=$(ini_parser "hyphae" "vent_off" $INIFILE)
    HVON=$(ini_parser "hyphae" "vent_on" $INIFILE)
    MHMAX=$(ini_parser "mushroom" "humidity_max" $INIFILE)
    MHMIN=$(ini_parser "mushroom" "humidity_min" $INIFILE)
    MLOFF=$(ini_parser "mushroom" "light_off" $INIFILE)
    MLON=$(ini_parser "mushroom" "light_on" $INIFILE)
    MTMAX=$(ini_parser "mushroom" "temperature_max" $INIFILE)
    MTMIN=$(ini_parser "mushroom" "temperature_min" $INIFILE)
    MVOFF=$(ini_parser "mushroom" "vent_off" $INIFILE)
    MVON=$(ini_parser "mushroom" "vent_on" $INIFILE)
  fi
}

saveconfig()
{
  echo '; cfg_example.ini' > $INIFILE
  echo '' >> $INIFILE
  echo '[hyphae]' >> $INIFILE
  echo "humidity_min=$HHMIN" >> $INIFILE
  echo "humidity_max=$HHMAX" >> $INIFILE
  echo "temperature_min=$HTMIN" >> $INIFILE
  echo "temperature_max=$HTMAX" >> $INIFILE
  echo "light_on=$HLON" >> $INIFILE
  echo "light_off=$HLOFF" >> $INIFILE
  echo "vent_on=$HVON" >> $INIFILE
  echo "vent_off=$HVOFF" >> $INIFILE
  echo '' >> $INIFILE
  echo '[mushroom]' >> $INIFILE
  echo "humidity_min=$MHMIN" >> $INIFILE
  echo "humidity_max=$MHMAX" >> $INIFILE
  echo "temperature_min=$MTMIN" >> $INIFILE
  echo "temperature_max=$MTMAX" >> $INIFILE
  echo "light_on=$MLON" >> $INIFILE
  echo "light_off=$MLOFF" >> $INIFILE
  echo "vent_on=$MVON" >> $INIFILE
  echo "vent_off=$MVOFF" >> $INIFILE
}

saveoutfile()
{
  mkdir --parents $PRGDIR
  mv --force $PYFILE $BAKFILE 2> /dev/null
  cat << EOF > $PYFILE
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

EOF
  echo '  # check growing mode:' >> $PYFILE
  echo '  if in3==1:' >> $PYFILE
  echo '    # growing hyphae' >> $PYFILE
  echo "    humidity_min=$HHMIN" >> $PYFILE
  echo "    humidity_max=$HHMAX" >> $PYFILE
  echo "    temperature_min=$HTMIN" >> $PYFILE
  echo "    temperature_max=$HTMAX" >> $PYFILE
  echo "    light_on=$HLON" >> $PYFILE
  echo "    light_off=$HLOFF" >> $PYFILE
  echo "    vent_on=$HVON" >> $PYFILE
  echo "    vent_off=$HVOFF" >> $PYFILE
  echo '  else:' >> $PYFILE
  echo '    # growing mushroom' >> $PYFILE
  echo "    humidity_min=$MHMIN" >> $PYFILE
  echo "    humidity_max=$MHMAX" >> $PYFILE
  echo "    temperature_min=$MTMIN" >> $PYFILE
  echo "    temperature_max=$MTMAX" >> $PYFILE
  echo "    light_on=$MLON" >> $PYFILE
  echo "    light_off=$MLOFF" >> $PYFILE
  echo "    vent_on=$MVON" >> $PYFILE
  echo "    vent_off=$MVOFF" >> $PYFILE
  cat << EOF >> $PYFILE

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
  if (m>vent_on) and (m<vent_off):
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
  outputs=str(out1)+str(out2)+str(out3)+str(out4)+ \\
          str(err1)+str(err2)+str(err3)+str(err4)
  return outputs
EOF
  chmod 755 $PYFILE
}

deltemp()
{
  rm --force /tmp/$$_1.tmp > /dev/null
  rm --force /tmp/$$_2.tmp > /dev/null
  rm --force /tmp/$$_3.tmp > /dev/null
}

inputbox()
{
  if [ $1 -eq 1 ]
  then
    case $2 in
      1) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU1" 3 50 0 100 "$HHMIN" 2> /tmp/$$_3.tmp;;
      2) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU2" 3 50 0 100 "$HHMAX" 2> /tmp/$$_3.tmp;;
      3) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU3" 3 50 0 40 "$HTMIN" 2> /tmp/$$_3.tmp;;
      4) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU4" 3 50 0 40 "$HTMAX" 2> /tmp/$$_3.tmp;;
      5) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU5" 3 50 0 23 "$HLON" 2> /tmp/$$_3.tmp;;
      6) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU6" 3 50 0 23 "$HLOFF" 2> /tmp/$$_3.tmp;;
      7) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU7" 3 50 0 59 "$HVON" 2> /tmp/$$_3.tmp;;
      8) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU8" 3 50 0 59 "$HVOFF" 2> /tmp/$$_3.tmp;;
    esac
    if [ $? -ne 0 ]; then return; fi
    RESULT=`cat /tmp/$$_3.tmp | sed s/' '//`
    case $2 in
      1) HHMIN=$RESULT;;
      2) HHMAX=$RESULT;;
      3) HTMIN=$RESULT;;
      4) HTMAX=$RESULT;;
      5) HLON=$RESULT;;
      6) HLOFF=$RESULT;;
      7) HVON=$RESULT;;
      8) HVOFF=$RESULT;;
    esac
  else
    case $2 in
      1) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU1" 3 50 0 100 "$MHMIN" 2> /tmp/$$_3.tmp;;
      2) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU2" 3 50 0 100 "$MHMAX" 2> /tmp/$$_3.tmp;;
      3) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU3" 3 50 0 40 "$MTMIN" 2> /tmp/$$_3.tmp;;
      4) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU4" 3 50 0 40 "$MTMAX" 2> /tmp/$$_3.tmp;;
      5) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU5" 3 50 0 23 "$MLON" 2> /tmp/$$_3.tmp;;
      6) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU6" 3 50 0 23 "$MLOFF" 2> /tmp/$$_3.tmp;;
      7) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU7" 3 50 0 59 "$MVON" 2> /tmp/$$_3.tmp;;
      8) dialog --backtitle "$BACKTITLE" --title "$TITLE" --rangebox "$MENU8" 3 50 0 59 "$MVOFF" 2> /tmp/$$_3.tmp;;
    esac
    if [ $? -ne 0 ]; then return; fi
    RESULT=`cat /tmp/$$_3.tmp | sed s/' '//`
    case $2 in
      1) MHMIN=$RESULT;;
      2) MHMAX=$RESULT;;
      3) MTMIN=$RESULT;;
      4) MTMAX=$RESULT;;
      5) MLON=$RESULT;;
      6) MLOFF=$RESULT;;
      7) MVON=$RESULT;;
      8) MVOFF=$RESULT;;
    esac
  fi
  sleep 2
}

hyphaeparams()
{
while true
do
  dialog --backtitle "$BACKTITLE" \
         --title "$TITLE" \
         --menu "Growing hyphae" 16 45 9 \
         1 "$MENU1" \
         2 "$MENU2" \
         3 "$MENU3" \
         4 "$MENU4" \
         5 "$MENU5" \
         6 "$MENU6" \
         7 "$MENU7" \
         8 "$MENU8" \
         9 "Back to main menu" 2> /tmp/$$_2.tmp
  if [ $? -eq 0 ]
  then
    case `cat /tmp/$$_2.tmp` in
      1)  inputbox 1 1;;
      2)  inputbox 1 2;;
      3)  inputbox 1 3;;
      4)  inputbox 1 4;;
      5)  inputbox 1 5;;
      6)  inputbox 1 6;;
      7)  inputbox 1 7;;
      8)  inputbox 1 8;;
      9)  return;;
  esac
  else
    return
  fi
done
}

mushroomparams()
{
while true
do
  dialog --backtitle "$BACKTITLE" \
         --title "$TITLE" \
         --menu "Growing mushroom" 16 45 9 \
         1 "$MENU1" \
         2 "$MENU2" \
         3 "$MENU3" \
         4 "$MENU4" \
         5 "$MENU5" \
         6 "$MENU6" \
         7 "$MENU7" \
         8 "$MENU8" \
         9 "Back to main menu" 2> /tmp/$$_2.tmp
  if [ $? -eq 0 ]
  then
    case `cat /tmp/$$_2.tmp` in
      1)  inputbox 2 1;;
      2)  inputbox 2 2;;
      3)  inputbox 2 3;;
      4)  inputbox 2 4;;
      5)  inputbox 2 5;;
      6)  inputbox 2 6;;
      7)  inputbox 2 7;;
      8)  inputbox 2 8;;
      9)  return;;
  esac
  else
    return
  fi
done
}

exitandrestartservice()
{
  saveoutfile;
  saveconfig;
  deltemp;
  dialog --backtitle "$BACKTITLE" --title "$TITLE" --infobox "Restart mm3d.py daemon." 3  27
  sleep 2
  clear;
  sudo /etc/init.d/mm3d.sh stop
  sudo /etc/init.d/mm3d.sh start
  exit 0
}

loadconfig
if ! type -all "dialog" > /dev/null 2>&1
then
  echo 'There is not dialog on your system!'
  exit 1
fi
while true
do
  dialog --backtitle "$BACKTITLE" \
         --title "$TITLE" \
         --menu "Main menu" 11 30 4 \
         1 "Growing hyphae" \
         2 "Growing mushroom" \
         3 "Save program" \
         4 "Save and exit" 2> /tmp/$$_1.tmp
  if [ $? -eq 0 ]
  then
    case `cat /tmp/$$_1.tmp` in
      1)  hyphaeparams;;
      2)  mushroomparams;;
      3)  saveoutfile;;
      4)  exitandrestartservice;;
    esac
    else
      deltemp
      clear
      exit 0
    fi
done
