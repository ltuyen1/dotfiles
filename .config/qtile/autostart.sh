#!/usr/bin/env bash 

# Essential stuffs.
picom --config ~/.config/qtile/picom.conf &
dunst -conf ~/.config/qtile/dunstrc  &
nm-applet &
blueman-applet &

# Sound
pipewire &
pipewire-pulse &
wireplumber &

# Wallpaper
# hsetroot -fill ~/.config/qtile/images/wall.jpg
# nitrogen --restore &
feh --bg-fill --randomize ~/Pictures/walls/ --no-fehbg

# Others
ibus-daemon -rdx &
xss-lock --transfer-sleep-lock slock &
xrdb -merge ~/.Xresources &
lxpolkit &
