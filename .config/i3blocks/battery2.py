#!/usr/bin/env python3
"""
 Copyright (C) 2016 James Murphy
 Licensed under the GPL version 2 only

 A battery indicator blocklet script for i3blocks
"""
# Requires: acpi

# pylint: disable=invalid-name

from subprocess import check_output
import os
import re
import sys

config = dict(os.environ)
status = check_output(['acpi'], universal_newlines=True)
health = check_output(['acpi', '-b', '-i'], universal_newlines=True)
#print(health.split('\n')[1].split(' ')[-1])

if not status:
    # stands for no battery found
    color = config.get("color_10", "red")
    fulltext = f"<span color='{color}'><span font='FontAwesome'>\uf00d \uf240</span></span>"
    percentleft = 100
else:
    # if there is more than one battery in one laptop, the percentage left is
    # available for each battery separately, although state and remaining
    # time for overall block is shown in the status of the first battery
    batteries = status.split("\n")
    state_batteries=[]
    commasplitstatus_batteries=[]
    percentleft_batteries=[]
    time = ""
    for battery in batteries:
        if battery!='':
            state_batteries.append(battery.split(": ")[1].split(", ")[0])
            commasplitstatus = battery.split(", ")
            if not time:
                time = commasplitstatus[-1].strip()
                # check if it matches a time
                time = re.match(r"(\d+):(\d+)", time)
                if time:
                    time = ":".join(time.groups())
                    timeleft = f" ({time})"
                else:
                    timeleft = ""

            p = int(commasplitstatus[1].rstrip("%\n"))
            if p>0:
                percentleft_batteries.append(p)
            commasplitstatus_batteries.append(commasplitstatus)
    state = state_batteries[0]
    commasplitstatus = commasplitstatus_batteries[0]
    if percentleft_batteries:
        percentleft = int(sum(percentleft_batteries)/len(percentleft_batteries))
    else:
        percentleft = 0

    # stands for charging
    color = config.get("color_charging", "yellow")
    FA_LIGHTNING = f"<span color='{color}'><span font='FontAwesome'>\uf0e7</span></span>"

    # stands for plugged in
    FA_PLUG = "<span font='FontAwesome'>\uf1e6</span>"

    # pylint: disable=too-many-return-statements
    def color(percent):
        """color"""
        if percent < 10:
            # exit code 33 will turn background red
            col = config.get("color_10", "#FFFFFF")
        elif percent < 20:
            col = config.get("color_20", "#FF3300")
        elif percent < 30:
            col = config.get("color_30", "#FF6600")
        elif percent < 40:
            col = config.get("color_40", "#FF9900")
        elif percent < 50:
            col = config.get("color_50", "#FFCC00")
        elif percent < 60:
            col = config.get("color_60", "#FFFF00")
        elif percent < 70:
            col = config.get("color_70", "#FFFF33")
        elif percent < 80:
            col = config.get("color_80", "#FFFF66")
        else:
            col = config.get("color_full", "#FFFFFF")
        return col

    def get_battery(percent):
        """get_battery"""
        col = color(percent)
        if percent < 10:
            # exit code 33 will turn background red
            sym = '\uf58d'  # empty
        elif percent < 20:
            sym = '\uf579'  # 10%
        elif percent < 30:
            sym = '\uf57a'  # 20
        elif percent < 40:
            sym = '\uf57b'  # 30
        elif percent < 50:
            sym = '\uf57c'  # 40
        elif percent < 60:
            sym = '\uf57d'  # 50
        elif percent < 70:
            sym = '\uf57e'  # 60
        elif percent < 80:
            sym = '\uf57f'  # 70
        elif percent < 90:
            sym = '\uf580'  # 80
        elif percent < 100:
            sym = '\uf581'  # 90
        else:
            sym = '\uf578'  # 100
        return f"<span color='{col}' font='mononoki Nerd Font Mono'>{sym}</span>"


    # stands for using battery
    #FA_BATTERY = "<span font='FontAwesome'>\uf240</span>"
    FA_BATTERY = get_battery(percentleft)

    # stands for unknown status of battery
    FA_QUESTION = "<span font='FontAwesome'>\uf128</span>"


    if state == "Discharging":
        fulltext = FA_BATTERY + " "
    elif state == "Full":
        fulltext = FA_PLUG + " "
        timeleft = ""
    elif state == "Unknown":
        fulltext = FA_QUESTION + " " + FA_BATTERY + " "
        timeleft = ""
    else:
        fulltext = FA_LIGHTNING + " " + FA_PLUG + " "

    form =  '<span color="{}">{}%</span>'
    fulltext += form.format(color(percentleft), percentleft)
    fulltext += timeleft
    fulltext += " ["+health.split('\n')[1].split(' ')[-1]+"]"

print(fulltext)
print(fulltext)

if percentleft < 10:
    sys.exit(33)
