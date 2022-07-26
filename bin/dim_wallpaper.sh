#!/bin/bash
#set -x
pictures=/home/judge/clones/wallpapers

opacity=0.65
shade=/tmp/out.png
input=${pictures}/boobs/sexy-african-pierced-nipples.png 
dimensions=$(identify "$input" |sed  's/.* \([0-9x]*\) .*/\1/g') 
result=$HOME/.config/sway/wallpapers/wallpaper_$$.png
wallpaper=0

dimmer()
{
  rm -f "$shade" "$result"

  # create a black image with opacity
  if ! convert -size "$dimensions" xc:'rgba(0, 0, 0, '$opacity')' "$shade"
  then
    echo "Problem with convert command."
    exit 1
  fi

  # overlay the transparent image onto the wallpaper image
  #convert $input -gravity center $shade -composite $result
  if ! composite "$shade" "$input" "$result"
  then
    echo "Problem with composite command."
    exit 1
  fi
}

set_wallpaper()
{
  #rm -f $shade
  if [ $wallpaper -eq 1 ]
  then
    cd ~/.config/sway/ || exit 1
    ln -sf "$result" wallpaper.png
    pid=$(pgrep swaybg)
    swaybg -m fill -i "wallpaper.png" 2>/dev/null &
    echo "$pid" | xargs kill
  fi
}

# -i input  -o output  -t transparency  -w (set as new wallpaper)
usage()
{
    echo "dim_wallpaper -i input.jpg -o output.jpg -t opacity  -w (set wallpaper)  -h"
}


while getopts "i:o:t:wh" OPTION; do
    case $OPTION in
        i) input="$OPTARG" ;;
        o) result="$OPTARG" ;;
        t) opacity="$OPTARG" ;;
        w) wallpaper=1 ;;
        h) usage; exit 2 ;;
        *) echo "Invalid Option [$OPTION]"; usage; exit 2 ;;
    esac
done
dimensions=$(identify "$input" |sed  's/.* \([0-9x]*\) .*/\1/g')

#echo "$input $result $opacity $wallpaper"
#echo $dimensions

#exit

dimmer
set_wallpaper

