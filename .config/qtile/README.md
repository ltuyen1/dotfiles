# My Qtile config


**qtile** is a tiling window manager for both X11 and Wayland written in python

Original config by [Derek Taylor](https://gitlab.com/dwt1) aka ([DistroTube](https://youtube.com/@DistroTube)), Modified by me!

Requires: qtile-extras, Symbols Nerd Font and also Iosevka Nerd Font

# Layouts

There are current layouts in this config:

- MonadTall
- MonadWide
- Tile
- Max
- Bsp
- TreeTab

# Bar

I'm not using third-party statusbar other than Qtile <br>
The qtile built-in statusbar was used as an status bar.

# Keybindings

The keybindings list was actually not complete

MODKEY is set to the Super key (aka the Windows Key)

| Keybinding | Action |
| :--- | :--- |
| `MODKEY + Tab` | Switch layout |
| `MODKEY + Enter` | Open terminal emulator (Default: st) |
| `MODKEY + [H, J, K, L]` | Switches focus between windows |
| `MODKEY + P` | Open app launcher |
| `MODKEY + Shift + Q` | Open logout prompt |
| `MODKEY + Shift + [H, J, K, L]` | Rotates the Window in the stack |
| `MODKEY + Shift + Space` | Toggle floating between window |
| `MODKEY + R` | Spawn command |
