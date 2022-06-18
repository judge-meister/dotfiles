#!/bin/bash

# Requires: yad

# shellcheck disable=2016
#grep -E 'bindsym|# KP_GROUP' .config/i3/config  | \
#  grep -v -E  'workspace|#|Print ' | \
#  sed 's|bindsym $mod+|Mod-|g;s|bindsym ||g;s|# KP_GROUP\(.*\)|\n\1|g' | \
#  yad --text-info --back=#282c34 --fore=#46d9ff --geometry=1000x600

if [ "$1" == "i3" ] || [ "$1" == "sway" ]
then
    WM=$1
else
    exit
fi
(
grep -E 'bindsym|^#=' ~/.config/"${WM}"/config \
    | grep -E '\$mod|Ctrl|Print|Shift|#=' | grep -v '#bindsym' \
    | sed -e 's/#=//g' \
          -e 's/exec //g' \
          -e 's/$mod/[Mod]/g' \
          -e 's/Shift/[Shift]/g' \
          -e 's/Ctrl/[Ctrl]/g' \
          -e 's/$term/Terminal Emulator/g' \
          -e 's/$drun_/Application /g' \
          -e 's/$run_/Program /g' \
          -e 's/$lockcmd/Screen Lock/g' \
          -e 's/Terminal.*update_packages/Update System Packages/g' \
    | awk -F' ' '{printf "%6s %-25s %s %s %s %s %s %s %s %s\n",$1,$2,$3,$4,$5,$6,$7,$8,$9,$10}' \
    | sed -e 's/bindsym/  /g'
grep -E '^#-' ~/.config/"${WM}"/config | sed 's|#-||g'
) \
 | yad --text-info --back=#282c34 --fore=#46d9ff --geometry=1000x600
