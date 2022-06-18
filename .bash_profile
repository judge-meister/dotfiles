#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

export PATH=~/bin:~/.local/bin:$PATH
export EDITOR=/usr/bin/vim
export XDG_CURRENT_DESKTOP=Unity

#[[ $(fgconsole 2>/dev/null) == 1 ]] && exec startgui
[[ $(fgconsole 2>/dev/null) == 1 ]] && tbsm
	
#exec startx -- vt1

