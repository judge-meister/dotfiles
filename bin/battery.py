#!/usr/bin/env python3
"""
battery status for i3block
"""
# pylint: disable=line-too-long,invalid-name
# unspecified-encoding

import os

BAT0 = '/sys/class/power_supply/BAT0'

def read_int_value(attr):
    """read int value"""
    val = -1
    attrpath = os.path.join(BAT0, attr)
    if os.path.exists(attrpath):
        with open(attrpath, 'r', encoding='utf-8') as fp:
            val = int(fp.readlines()[0])
    return val

def read_str_value(attr):
    """read str value"""
    val = ''
    attrpath = os.path.join(BAT0, attr)
    if os.path.exists(attrpath):
        with open(attrpath, 'r', encoding='utf-8') as fp:
            val = fp.readlines()[0][:-1]
    return val

def low_battery(capacity):
    """low battery"""
    HOME = os.environ['HOME']
    __icon = f'--icon="{HOME}/.local/share/icons/battery_low_dark.png" '
    cmd = f'notify-send {__icon} "Very Low Battery" "Only {capacity}% battery remaining.\nFind a power brick now."'
    os.system(cmd)

Alarm = read_int_value('alarm')
ChargeNow = read_int_value('energy_now')
ChargeFull = read_int_value('energy_full')
ChargeFullDesign = read_int_value('energy_full_design')
Status = read_str_value('status')
#print(Alarm, ChargeNow, ChargeFull)

Percent = min(ChargeNow * 100 / ChargeFull, 100.0)
#if Percent > 100.0:
#    Percent = 100.0

#print("[%s]" % Status)

Result = f"{Percent:2.0f}%"

if ChargeNow <= Alarm and Status == "Discharging":
    low_battery(Percent)
    Status = "Low Battery"

if ChargeNow >= ChargeFull:
    Status = "Charged"

print(f"{Result} {Status}")
