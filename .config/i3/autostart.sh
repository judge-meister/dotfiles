#!/bin/bash
#
# start some stuff for i3
#
# Requires: dunst, lxsession, picom, networkmanager, volumeicon, feh

VENDOR="$(cat /sys/class/dmi/id/sys_vendor)"

dunst &
lxsession & 
~/.fehbg &
picom -CGb
if [ "$VENDOR" = "LENOVO" ]; then
    setxkbmap -layout gb ;
    
elif [ "$VENDOR" = "Apple Inc." ]; then
    setxkbmap -layout gb -model macbook79 ;
    "$HOME"/bin/macfnmode fn ; 
    
fi 
nm-applet &
volumeicon &
udiskie -ant &

