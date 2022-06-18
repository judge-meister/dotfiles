#!/bin/bash
# Requires: bc, acpi, acpid

VENDOR=$(cat /sys/class/dmi/id/sys_vendor)

if [ "$VENDOR" == "Apple Inc." ]
then
  #TEMP_INPUT="/sys/class/hwmon/hwmon3/temp2_input"
  TEMP_INPUT="/sys/class/hwmon/hwmon1/temp1_input"
  t=$(cat $TEMP_INPUT); 
  echo "$t / 1000" | bc -s | awk '{print " "$1"°C"}'; 

  if [ "$t" -gt 75000 ];
  then 
    exit 33; 
  fi; 

elif [ "$VENDOR" == "LENOVO" ]
then
  #TEMP_INPUT="/sys/class/hwmon/hwmon1/temp1_input"
  TEMP=$(acpi -t | awk -F' ' '{print $4}' | sed 's/.0//g')
  echo " ${TEMP}°C"
  if [ $((TEMP)) -gt 80 ]
  then
    exit 33
  fi
fi

exit 0

