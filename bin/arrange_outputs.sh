#!/bin/bash

#set -x

OUTPUTS=($(swaymsg -t get_outputs -r | jq '.[].name'))

function output_options()
{
  c=1
  for out in ${OUTPUTS[@]}
  do
    echo "    ${c}. $out"
    c=$((c+1))
  done
  echo -n ": "
}

function horizontal_output()
{
  
    echo "Horizontal ${OUTPUTS[$1]} ${OUTPUTS[$2]}"
    WIDTH=$(swaymsg -t get_outputs -r | jq '.['$1'].rect.width')
    #set -x
    swaymsg output ${OUTPUTS[$1]} pos 0 0
    swaymsg output ${OUTPUTS[$2]} pos $WIDTH 0
    #set +x
}

function vertical_output()
{
    echo "Vertical ${OUTPUTS[$1]} ${OUTPUTS[$2]}"
    HEIGHT=$(swaymsg -t get_outputs -r | jq '.['$1'].rect.height')
    #set -x
    swaymsg output ${OUTPUTS[$1]} pos 0 0
    swaymsg output ${OUTPUTS[$2]} pos 0 $HEIGHT 
    #set +x
}

if [ "${#OUTPUTS[@]}" -eq 1 ]
then
  echo "Single output only."
  swaymsg output ${OUTPUTS[$1]} pos 0 0
  exit
fi

echo -en "Arrange Outputs Horizontal or Vertical [h/v]: "
read ans
if [ "${ans,,}" == "h" ]
then
  ORIENTATION="horiz"
  echo -e "Which display to the left ? "
  output_options
  read first
  echo -e "Which display to the right ? "
  output_options
  read second
  horizontal_output $((first-1)) $((second-1))
  
elif [ "${ans,,}" == "v" ]
then
  ORIENTATION="vert"
  echo -e "Which display at the top ? "
  output_options
  read top
  echo -e "Which display at the bottom ? "
  output_options
  read bottom
  vertical_output $((top-1)) $((bottom-1))
fi


