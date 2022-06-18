#!/bin/bash

list_missing_packages()
{
  # shellcheck disable=SC2162
  #sort -u pkglist.txt | grep -v '#' | while read x; 
  grep -v -E 'pacman|#|}|{' install_pkgs.sh | sort -u | awk -F' ' '{print $1}' | while read x;
  do 
    if [ "x$x" != "x" ]; 
    then 
      if ! pacman -Q | grep "^$x" > /dev/null; 
      then 
        echo "$x"; 
      fi;
    fi; 
  done
}


