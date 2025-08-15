## Left Prompt
function fish_prompt
	# Show the current working directory
	set_color black
	if test (id -u) -eq 0
		set_color --background=yellow
	else
		set_color --background=green
	end
	echo -n ' '
	echo -n (prompt_pwd)
	echo -n ' '
	set_color normal
	echo -n ' '
end

## Window title
function fish_title
	echo -n 'fish in '
	prompt_pwd
end

## Variables
set HISTCONTROL ignoreboth
set HISTSIZE 1000
set HISTFILESIZE 2000

source ~/.alias

set PATH "$HOME/bin:$HOME/.local/bin:$PATH"

## Keybinding
set fish_key_bindings fish_default_key_bindings
