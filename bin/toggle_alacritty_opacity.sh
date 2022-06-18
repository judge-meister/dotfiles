#!/usr/bin/env bash
# Requires: libnotify, alacritty

set -x
exec &> >(tee -a ~/bin/toggle_al_op.log)
echo "-----------------------------------"
## If alacritty.yml does not exist, raise an alert
[[ ! -f ~/.config/alacritty/alacritty.yml ]] && \
    notify-send "alacritty.yml does not exist" && exit 0

## Fetch background_opacity from alacritty.yml
opacity=$(awk '$1 == "opacity:" {print $2; exit}' \
    ~/.config/alacritty/alacritty.yml)
echo "$1 $opacity"
case $1 in 
  -i) toggle_opacity=$(printf "%.2f" "$(echo "$opacity+0.05" | bc)")
      ;;
  -d) toggle_opacity=$(printf "%.2f" "$(echo "$opacity-0.05" | bc)")
      ;;
esac
echo "$opacity > $toggle_opacity"

## Assign toggle opacity value
case $toggle_opacity in
  1.05) toggle_opacity=1.0
       ;;
  -0.05) toggle_opacity=0.0
       ;;
esac
echo "$opacity > $toggle_opacity"

## Replace opacity value in alacritty.yml
sed -i -- "s/opacity: $opacity/opacity: $toggle_opacity/" \
    ~/.config/alacritty/alacritty.yml

cp ~/.config/alacritty/alacritty.yml ~/clones/dotfiles/.config/alacritty/alacritty.yml
