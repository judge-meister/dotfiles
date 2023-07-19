#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

export PATH=~/bin:~/.local/bin:$PATH
export EDITOR=/usr/bin/vim
export XDG_CURRENT_DESKTOP=Unity
export XDG_DATA_HOME=$HOME/.local/share
export XDG_CONFIG_HOME=$HOME/.config
export XDG_STATE_HOME=$HOME/.local/state
export XDG_CACHE_HOME=$HOME/.cache
export QT_QPA_PLATFORMTHEME=qt5ct
#export PYOPENGL_PLATFORM=x11
export PYOPENGL_PLATFORM=egl

#export OPENER=
export IMAGER=swayimg

# some variables for hikari
export TERMINAL=/sbin/foot
export BROWSER=/sbin/firefox-developer-edition

# set keyboard layout for river
export XKB_DEFAULT_LAYOUT="gb"

#[[ $(fgconsole 2>/dev/null) == 1 ]] && exec startgui
[[ $(fgconsole 2>/dev/null) == 1 ]] && tbsm
	
#exec startx -- vt1

