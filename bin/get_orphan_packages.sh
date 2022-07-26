#!/bin/bash

pacman -Q | cut -d' ' -f1 | while read -r x
do 
  if pacman -Qi "$x" | grep -q 'Installed as a dependency' >/dev/null
  then
    if pacman -Qi "$x" | grep -q 'Required By.*: None' >/dev/null
    then 
      echo "$x"
    fi
  fi
done

