# Source the alias file
source ~/.alias

# History settings
shopt -s histappend
shopt -s histverify
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000

# Autocompletion
shopt -s extglob
shopt -s autocd

# Sourcing
source ~/.profile

# Prompt
PROMPT_DIRTRIM=2
PS1='\[\e[0m\][$HOSTNAME]\[\e[0m\] \[\e[0;32m\]\w\[\e[0m\] \[\e[0m\]\$\[\e[0m\] '
