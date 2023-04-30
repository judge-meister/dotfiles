#!/bin/bash

# ~/Videos/lexa-sorted.m3u
# or given video file
PLAYLIST=$HOME/Videos/lexa-sorted.m3u
OUTPUT_0=$(swaymsg -t get_outputs | jq '.[0].name' | sed 's/"//g' )
#OUTPUT_0_FOCUSED=$(swaymsg -t get_outputs | jq '.[0].focused')
OUTPUT_1=$(swaymsg -t get_outputs | jq '.[1].name' | sed 's/"//g' )
OUTPUT_1_FOCUSED=$(swaymsg -t get_outputs | jq '.[1].focused')

#echo "$OUTPUT_0 $OUTPUT_0_FOCUSED"
#echo "$OUTPUT_1 $OUTPUT_1_FOCUSED"

if [ "$OUTPUT_1_FOCUSED" == "true" ]; then 
    OUTPUT=$OUTPUT_1
else
    OUTPUT=$OUTPUT_0
fi

case $1 in
  start) shift;;
  quit) ~/.swaybgrc
        #random_swaybg.py "$HOME"/.config/sway/wallpaper.png; 
        pkill mpvpaper;
        swaymsg mode default;
        exit;;
  pause|play) echo 'cycle pause' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  mute|unmute) echo 'cycle mute' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  fore5) echo 'keypress right' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  back5) echo 'keypress left' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  fore60) echo 'keypress up' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  back60) echo 'keypress down' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  speedup) echo 'keypress ]' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  slowdown) echo 'keypress [' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  info) echo 'keypress i' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  osd) echo 'keypress o' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  next) echo 'keypress >' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
  prev) echo 'keypress <' | socat - "/tmp/mpv-socket-$OUTPUT"; exit;;
esac

SINGLE=""
if [ $# -gt 0 ]
then
  # shellcheck disable=SC2124
  SINGLE="$@"
fi

pgrep swaybg|xargs kill
pgrep mpvpaper|xargs kill

if [ "$SINGLE" == "" ]
then
    mpvpaper -p -o "--loop-playlist shuffle input-ipc-server=/tmp/mpv-socket-$OUTPUT" "$OUTPUT" "$PLAYLIST"
else
    mpvpaper -p -o "input-ipc-server=/tmp/mpv-socket-$OUTPUT" "$OUTPUT" "$SINGLE"
    ~/.swaybgrc
        #random_swaybg.py "$HOME"/.config/sway/wallpaper.png; 
    pkill mpvpaper;
    swaymsg mode default;
    exit
fi

