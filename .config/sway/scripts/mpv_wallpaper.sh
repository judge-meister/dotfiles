#!/bin/bash

# ~/Videos/lexa-sorted.m3u
# or given video file
PLAYLIST=$HOME/Videos/lexa-sorted.m3u
OUTPUT=LVDS-1

case $1 in
  start) shift;;
  quit) random_swaybg.py "$HOME"/.config/sway/wallpaper.png; 
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
esac

if [ $# -gt 0 ]
then
  # shellcheck disable=SC2124
  PLAYLIST="$@"
fi

pgrep swaybg|xargs kill
pgrep mpvpaper|xargs kill

mpvpaper -p -o "--loop-playlist shuffle input-ipc-server=/tmp/mpv-socket-$OUTPUT" $OUTPUT "$PLAYLIST"

