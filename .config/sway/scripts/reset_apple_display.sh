#!/bin/bash

function reset_apple_cinema()
{
    echo "reseting Apple Cinema Display"
    swaymsg output DP-1 disable
    sleep 0.5
    swaymsg output DP-1 enable
}

reset_apple_cinema

