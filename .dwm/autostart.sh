#!/bin/bash
set -x

#VENDOR="$(cat /sys/class/dmi/id/sys_vendor)"
PRODUCT="$(cat /sys/class/dmi/id/product_name)"
FAMILY="$(cat /sys/class/dmi/id/product_family)"



if [ "$FAMILY" == "ThinkPad X230" ]; #if [ "$VENDOR" == "LENOVO" ]; 
then
    setxkbmap -layout gb ;
    ~/.fehbg & 
    #nitrogen --restore &
 
elif [ "$PRODUCT" == "MacBookPro5,5" ]; #elif [ "$VENDOR" == "Apple Inc." ];
then
    setxkbmap -layout gb -model macbook79 ;
    ~/.fehbg & 
    "$HOME"/bin/macfnmode media ;
fi ;

lxsession &
picom -CGb
dwmblocks &

xbindkeys &

