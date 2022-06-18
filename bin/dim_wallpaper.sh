#!/bin/bash
set -x
pictures=/home/judge/Pictures/WP

opacity=0.65
shade=out.png
input=sexy-african-pierced-nipples.png 
dimensions=$(identify "$pictures"/"$input" |sed  's/.* \([0-9x]*\) .*/\1/g') 
result=result.png

dimmer()
{
  rm -f $shade $result

  # create a black image with opacity
  convert -size "$dimensions" xc:'rgba(0, 0, 0, '$opacity')' $pictures/$shade

  # overlay the transparent image onto the wallpaper image
  #convert $input -gravity center $shade -composite $result
  composite $pictures/$shade $pictures/$input $pictures/$result

  #rm -f $shade

  pid=$(pgrep swaybg)
  swaybg -m fill -i $pictures/$result 2>/dev/null &
  kill "$pid"
}

if [ "$#" -eq 2 ]
then
    opacity="$1"
    input="$2"
    dimensions=$(identify "$pictures"/"$input" |sed  's/.* \([0-9x]*\) .*/\1/g')
    dimmer
else
    dimmer
fi
