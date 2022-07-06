#!/bin/bash

find ~/ -type l 2>/dev/null | grep -v clone | while read -r x
do 
    if readlink "$x" | grep -q clones/dotfiles
    #if [ $? -eq 0 ]
    then 
        echo "$x"
    fi
done

