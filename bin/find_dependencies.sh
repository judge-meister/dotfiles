#!/bin/bash

#set -x
cd ~/ || exit

# shellcheck disable=SC2013
for x in  $( grep -E '# Requires:|// Requires:' "$HOME"/bin/* "$HOME"/.config/*/* "$HOME"/.local/bin/* 2>/dev/null \
     | grep -v 'find_dependencies.sh' \
     | awk -F':' '{print $3}' \
     | sed 's|,||g;s|(optional)||g' )
do 
  echo "$x"
done | sort -u
 
