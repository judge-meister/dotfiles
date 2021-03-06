#
# ~/.bashrc
#

export TERM="xterm-256color"

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

. ~/.bash_aliases
. ~/.bash_ls_colors

PS1='[\u@\h \W]\$ '

# set prompt (1 for bold, 0 for normal)
. ~/bin/command_prompt.sh 1
