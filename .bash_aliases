# My aliases

alias ls='ls -G --color=auto '
#alias ls='exa --color=auto'

alias grep='grep --color=auto '
alias egrep='egrep --color=auto '
#alias more='less'

alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'

alias df='df -h'
alias free='free -m'

#alias vi='vim'

alias pacman='pacman --color auto '
alias yay='yay --color auto '

alias gst='git status'
alias gad='git add'
alias gcm='git commit -m'
alias gdt='git icdiff'

alias git-untracked='git ls-files --others '
alias git-tracked='git ls-tree --name-only -r HEAD'

alias ddd='kdbg'

function getappid()
{
  swaymsg -t get_tree | grep -E 'class|app_id' | grep -v null | awk -F' ' '{print $1 $2}' | sort -u
}


