#!/bin/bash

pacman -Q | cut -d' ' -f1 | while read -r x
do 
  if pacman -Qi "$x" | grep -q 'Explicitly installed' >/dev/null
  then 
    echo "$x"
  fi
done
