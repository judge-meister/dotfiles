#!/bin/bash
#
# Command Prompt
#
# Requires: git
#
# shellcheck disable=SC2034

# define the colour codes - the actual colours are picked up from the 
#                           terminal emulator theme

BLACK='\e[0;30m'
DARKRED='\e[0;31m'
DARKGREEN='\e[0;32m'
BROWN='\e[0;33m'
DARKBLUE='\e[0;34m'
PURPLE='\e[0;35m'
CYAN='\e[0;36m'
LIGHTGREY='\e[0;37m'

DARKGREY='\e[01;30m'
RED='\e[01;31m'
GREEN='\e[01;32m'
YELLOW='\e[01;33m'
BLUE='\e[01;34m'
PINK='\e[01;35m'
LIGHTCYAN='\e[01;36m'
WHITE='\e[01;37m'

NOCOL='\e[00m'

# function pinched from http://github.com/jessfraz/dotfiles/.bash_prompt
prompt_git() {
	local s='';
	local branchName='';

	# Check if the current directory is in a Git repository.
	if [ "$(git rev-parse --is-inside-work-tree &>/dev/null; echo "${?}")" == '0' ]; then

		# check if the current directory is in .git before running git checks
		if [ "$(git rev-parse --is-inside-git-dir 2> /dev/null)" == 'false' ]; then

			if [[ -O "$(git rev-parse --show-toplevel)/.git/index" ]]; then
				git update-index --really-refresh -q &> /dev/null;
			fi;

			# Check for uncommitted changes in the index.
			if ! git diff --quiet --ignore-submodules --cached; then
				s+='+';
			fi;

			# Check for unstaged changes.
			if ! git diff-files --quiet --ignore-submodules --; then
				s+='!';
			fi;

			# Check for untracked files.
			if [ -n "$(git ls-files --others --exclude-standard)" ]; then
				s+='?';
			fi;

			# Check for stashed files.
			if git rev-parse --verify refs/stash &>/dev/null; then
				s+='$';
			fi;

		fi;

		# Get the short symbolic ref.
		# If HEAD isn’t a symbolic ref, get the short SHA for the latest commit
		# Otherwise, just give up.
		branchName="$(git symbolic-ref --quiet --short HEAD 2> /dev/null || \
			git rev-parse --short HEAD 2> /dev/null || \
			echo '(unknown)')";

		[ -n "${s}" ] && s=" [${s}]";

		echo -e "${1}${branchName}${BLUE}${s}";
	else
		return;
	fi;
}


# command_prompt components

# red time and date
__date__="\[${DARKRED}\]\d \t "

# green user@host
__user_host__="\[${DARKGREEN}\]\u\[${YELLOW}\]@\[${DARKGREEN}\]\h\[${NOCOL}\]"

# cyan working dir  
__working_dir__=" \[${DARKBLUE}\]\w\[${NOCOL}\]"

# yellow open and close bracket
__close_bracket__="\[${YELLOW}\]] "
__open_bracket__="\[${YELLOW}\]["

# yellow [command number]
__comm_num__="\[${YELLOW}\][\!]\[${NOCOL}\]"

# add final $
__end=" \$ "


# construct PS1

PS1="$__date__"
PS1+="$__open_bracket__"
PS1+="$__user_host__"
PS1+="$__working_dir__"
PS1+="$__close_bracket__"
PS1+="\$(prompt_git \"\[${BROWN}\]\")"
PS1+="\n"
PS1+="$__comm_num__"
PS1+="$__end"

#PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD}\007"'
PROMPT_COMMAND='echo -ne "\033]0;${TERM}: ${PWD}\007"'

