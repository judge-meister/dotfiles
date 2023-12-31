#!/bin/bash

# this will move a container to a new workspace and then m ove that workspace
# to a designated output
#
# to use add the following bindsym to you sway/config
#
# bindsym $mod+Ctrl+1 move_browser_window 1 left
# bindsym $mod+Ctrl+2 move_browser_window 2 right


WKSPC=$1
LEFT_OR_RIGHT=$2

echo "$WKSPC  $LEFT_OR_RIGHT" >> ~/mbw.log

#workspace=$(swaymsg -t get_workspaces -r |jq '.[]| select(.focused == true).num')
#echo "focused workspace $workspace"

#output=$(swaymsg -t get_workspaces -r |jq '.[]| select(.focused == true).output')
#echo "focused output $output"
#if [ $(swaymsg -t get_outputs -r |jq '.[]| select(.name == '${output}').rect.x') -eq 0 ]
#then
#  monitor=left
#else
#  monitor=right
#fi

# get left and right output names
if [ $(swaymsg -t get_outputs -r |jq '.[0].rect.x') == 0 ]
then
  LEFT=$(swaymsg -t get_outputs -r |jq '.[0].name')
  RIGHT=$(swaymsg -t get_outputs -r |jq '.[1].name')
else
  LEFT=$(swaymsg -t get_outputs -r |jq '.[1].name')
  RIGHT=$(swaymsg -t get_outputs -r |jq '.[0].name')
fi

#container=$(swaymsg -t get_tree -r |jq '.. |select(.type?) | select(.focused == true).id')
#echo "focused container $container"


swaymsg "move container to workspace ${WKSPC}"
swaymsg "workspace number ${WKSPC}"
swaymsg "layout tabbed"

if [ "$LEFT_OR_RIGHT" = "left" ]
then
  swaymsg "move workspace to output ${LEFT}"
elif [ "$LEFT_OR_RIGHT" == "right" ]
then
  swaymsg "move workspace to output ${RIGHT}"
else
  swaymsg "move workspace to output ${LEFT}"
fi

