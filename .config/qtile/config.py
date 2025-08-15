import os
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
import colors

mod = "mod4"              # Sets mod key to SUPER/WINDOWS

# Terminal
myTerm = "st"

# Allows you to input a name when adding treetab section.
@lazy.layout.function
def add_treetab_section(layout):
    prompt = qtile.widgets_map["prompt"]
    prompt.start_input("Section name: ", layout.cmd_add_section)

# A function for hide/show all the windows in a group
@lazy.function
def minimize_all(qtile):
    for win in qtile.current_group.windows:
        if hasattr(win, "toggle_minimize"):
            win.toggle_minimize()
           
# A function for toggling between MAX and MONADTALL layouts
@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == 'monadtall':
        qtile.current_group.layout = 'max'
    elif current_layout_name == 'max':
        qtile.current_group.layout = 'monadtall'

keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Terminal"),
    Key([mod], "p", lazy.spawn("rofi -show drun -show-icons -config ~/.config/qtile/rofi/config.rasi"), desc='Run Launcher'),
    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggles the bar to show/hide"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.spawn("rofi -show p -modi p:'~/.local/bin/powermenu --no-symbols' -config ~/.config/qtile/rofi/powermenu.rasi"), desc="Logout menu"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "T", lazy.spawn("conky-toggle"), desc="Conky toggle on/off"),
    Key([mod], "end", lazy.window.bring_to_front(), desc="Bring window to the front"), # Mouse2 dont work on this my mouse, so Super+Esc used

    # Screenshot, Audio, Backlight, Media keys
    Key(
		[], "Print", 
		lazy.spawn('flameshot gui'),
		desc="Manual screenshot"
	),
    Key(
		["control"], "Print", 
		lazy.spawn('flameshot full'),
		desc="Take full screenshot"
	),
    Key(
		[], "XF86MonBrightnessUp", 
		lazy.spawn('brightnessctl set 5%+'),
		desc="Increase display brightness"	
	),
    Key(
		[], "XF86MonBrightnessDown", 
		lazy.spawn('brightnessctl set 5%-'),
		desc="Decrease display brightness"	
	),
    Key(
		[], "XF86AudioRaiseVolume", 
		lazy.spawn('amixer set Master 5%+'),
		desc="Raise speaker volume"	
	),
    Key(
		[], "XF86AudioLowerVolume", 
		lazy.spawn('amixer set Master 5%-'),
		desc="Lower speaker volume"	
	),
    Key(
		[], "XF86AudioMute", 
		lazy.spawn('amixer set Master toggle'),
		desc="Toggle mute"	
	),
    Key(
		[], "XF86AudioMicMute", 
		lazy.spawn('amixer set Capture toggle'),
		desc="Toggle microphone mute"	
	),
    Key(
		[], "XF86AudioNext", 
		lazy.spawn("playerctl next"),
		desc="Next track"
	),
    Key(
		[], "XF86AudioPrev", 
		lazy.spawn("playerctl previous"),
		desc="Previous track"
	),
    Key(
		[], "XF86AudioPlay", 
		lazy.spawn("playerctl play-pause"),
		desc="Toggle play/pause"
	),
    Key(
		[], "XF86AudioStop", 
		lazy.spawn("playerctl stop"),
		desc="Stop playing"
	),
    # Switch between windows
    # Some layouts like 'monadtall' only need to use j/k to move
    # through the stack, but other layouts like 'columns' will
    # require all four directions h/j/k/l to move around.
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h",
        lazy.layout.shuffle_left(),
        lazy.layout.move_left().when(layout=["treetab"]),
        desc="Move window to the left/move tab left in treetab"),

    Key([mod, "shift"], "l",
        lazy.layout.shuffle_right(),
        lazy.layout.move_right().when(layout=["treetab"]),
        desc="Move window to the right/move tab right in treetab"),

    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down().when(layout=["treetab"]),
        desc="Move window down/move down a section in treetab"
    ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up().when(layout=["treetab"]),
        desc="Move window downup/move up a section in treetab"
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "t", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Treetab prompt
    Key([mod, "shift"], "a", add_treetab_section, desc='Prompt to add new section in treetab'),

    # Grow/shrink windows left/right. 
    # This is mainly for the 'monadtall' and 'monadwide' layouts
    # although it does also work in the 'bsp' and 'columns' layouts.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),

    # Grow windows up, down, left, right.  Only works in certain layouts.
    # Works in 'bsp' and 'columns' layout.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.layout.maximize(), desc='Toggle between min and max sizes'),
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc='toggle floating'),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='toggle fullscreen'),
    Key([mod, "shift"], "m", minimize_all(), desc="Toggle hide/show all windows on current group"),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc='Move focus to next monitor'),
    Key([mod], "comma", lazy.prev_screen(), desc='Move focus to prev monitor'),
    
]

groups = []
group_names = ["1", "2", "3", "4", "5", "6"]
1
# Uncomment only one of the following lines
# group_labels = ["", "", "👁", "", "", "", "✀", "꩜", "", "⎙"]
group_labels = ["I", "II", "III", "IV", "V", "VI"]
#group_labels = ["DEV", "WWW", "SYS", "DOC", "VBOX", "CHAT", "MUS", "VID", "GFX", "MISC"]

# The default layout for each of the 10 workspaces
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))
 
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

colors = colors.Dark

layout_theme = {"border_width": 2,
                "margin": 5,
                "border_focus": colors[6],
                "border_normal": colors[9]
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Tile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.TreeTab(
         font = "Iosevka Nerd Font",
         fontsize = 20,
         border_width = 0,
         bg_color = colors[0],
         active_bg = colors[6],
         active_fg = colors[0],
         inactive_bg = colors[1],
         inactive_fg = colors[0],
         padding_x = 8,
         padding_y = 8,
         sections = ["One", "Two", "Three"],
         section_fontsize = 20,
         section_fg = colors[1],
         section_top = 15,
         section_bottom = 15,
         level_shift = 8,
         vspace = 3,
         panel_width = 150
    ),
    # layout.Floating(**layout_theme)
]

# Requires: qtile-extras
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras import widget

widget_defaults = dict(
    padding = 0,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Spacer(length = 7),
        widget.TextBox(
                 text = '󰛼',
                 font = "Symbols Nerd Font",
                 foreground = colors[0],
                 decorations = [
                    RectDecoration(colour=colors[5], radius=0, filled=True, padding_y=7, padding_x=0, group=True)
                 ],
                 padding = 10,
                 fontsize = 24
                 ),
        widget.CurrentLayout(
                 decorations = [
                    RectDecoration(colour=colors[10], radius=0, filled=True, padding_y=7, padding_x=0, group=True)
                 ],
                 foreground = colors[1],
                 font = 'Iosevka Nerd Font',
                 padding = 10,
                 fontsize = 18,
                 ),
        widget.GroupBox(
                 fontsize = 18,
                 margin_y = 5,
                 margin_x = 12,
                 padding_y = 0,
                 padding_x = 0,
                 borderwidth = 3,
                 active = colors[6],
                 inactive = colors[9],
                 font = 'Iosevka Nerd Font',
                 rounded = False,
                 highlight_color = colors[0],
                 highlight_method = "line",
                 this_current_screen_border = colors[6],
                 this_screen_border = colors [0],
                 other_current_screen_border = colors[6],
                 other_screen_border = colors[0],
                 ),
        widget.Spacer(length = -12),
        widget.TextBox(
                 text = '|',
                 foreground = colors[1],
                 font = 'Iosevka Nerd Font', 
                 padding = 7,
                 fontsize = 18
                 ),
        widget.Prompt(
                 font = 'Iosevka Nerd Font', 
                 fontsize = 18,
                 foreground = colors[1]
        ),
        widget.WindowName(
                 foreground = colors[1],
                 padding = 4,
                 font = 'Iosevka Nerd Font',
                 fontsize = 18,
                 max_chars = 30
                 ),
        widget.Systray(padding = 5, icon_size = 28),
        widget.Spacer(length = 10),
        widget.TextBox(
                 text = '|',
                 foreground = colors[1],
                 font = 'Iosevka Nerd Font',
                 padding = 0,
                 fontsize = 18
                 ),
        widget.TextBox(
                 text = ' ',
                 font = "Symbols Nerd Font",
                 foreground = colors[3],
                 padding = 7,
                 fontsize = 24
                 ),
        widget.ThermalSensor(
            foreground = colors[1],
            padding = 1,
            fontsize = 18,
            font = 'Iosevka Nerd Font',
            format = '{temp:.0f}{unit}'
        ),
        widget.Spacer(length = 15),
        widget.TextBox(
                 text = '󰕾',
                 font = "Symbols Nerd Font",
                 foreground = colors[0],
                 padding = 10,
                 decorations = [
                   RectDecoration(colour=colors[4], radius=0, filled=True, padding_y=7, padding_x=0, group=True)
                 ],
                 fontsize = 24
                 ),
        widget.Volume(
                 foreground = colors[1],
                 padding = 8, 
                 fontsize = 18,
                 font = 'Iosevka Nerd Font', 
                 fmt = '{}',
                 decorations = [
                   RectDecoration(colour=colors[10], radius=0, filled=True, padding_y=7, padding_x=0, group=True)
                 ],
                 ),
        widget.Spacer(length = 5),
        widget.Clock(
                 foreground = colors[1],
                 padding = 10,
                 fontsize = 18,
                 font = 'Iosevka Nerd Font', 
                 ## Uncomment for date and time 
                 # format = "⧗  %a, %b %d - %H:%M",
                 ## Uncomment for time only
                 decorations = [
                    RectDecoration(colour=colors[10], radius=0, filled=True, padding_y=7, padding_x=0, group=True)
                 ],
                 format = "%a %d %b",
                 ),
        widget.Clock(
                 foreground = colors[0],
                 padding = 10,
                 fontsize = 18,
                 font = 'Iosevka Nerd Font',
                 ## Uncomment for date and time 
                 # format = "⧗  %a, %b %d - %H:%M",
                 ## Uncomment for time only
                 decorations = [
                    RectDecoration(colour=colors[6], radius=0, filled=True, padding_y=7, padding_x=0, group=True)
                 ],
            format = "%I:%M %p",
                 ),
        widget.Spacer(length = 7),
        ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1 

# All other monitors' bars will display everything but widgets 22 (systray) and 23 (spacer).
def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[16:17]
    return widgets_screen2

# For adding transparency to your bar, add (background="#00000000") to the "Screen" line(s)
# For ex: Screen(top=bar.Bar(widgets=init_widgets_screen2(), background="#00000000", size=24)),

def init_screens():
    return [Screen(bottom=bar.Bar(widgets=init_widgets_screen1(), margin=[0, 0, 0, 0], size=50)),
            Screen(bottom=bar.Bar(widgets=init_widgets_screen2(), margin=[0, 0, 0, 0], size=50)),
            Screen(bottom=bar.Bar(widgets=init_widgets_screen2(), margin=[0, 0, 0, 0], size=50))]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    # Drag(["mod1"], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    # Drag(["mod1"], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    # Click(["mod1"], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors[4],
    border_width=1,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),   # gitk
        Match(wm_class="dialog"),         # dialog boxes
        Match(wm_class="download"),       # downloads
        Match(wm_class="error"),          # error msgs
        Match(wm_class="file_progress"),  # file progress boxes
        Match(wm_class='kdenlive'),       # kdenlive
        Match(wm_class="makebranch"),     # gitk
        Match(wm_class="maketag"),        # gitk
        Match(wm_class="notification"),   # notifications
        Match(wm_class="mpv"),            # mpv
        Match(wm_class="lxappearance"),   # LXappearance
        Match(wm_class='pinentry-gtk-2'), # GPG key password entry
        Match(wm_class="ssh-askpass"),    # ssh-askpass
        Match(wm_class="toolbar"),        # toolbars
        Match(wm_class="Yad"),            # yad boxes
        Match(title="branchdialog"),      # gitk
        Match(title='Confirmation'),      # tastyworks exit box
        Match(title='Qalculate!'),        # qalculate-gtk
        Match(title="pinentry"),          # GPG key password entry
        Match(title="tastycharts"),       # tastytrade pop-out charts
        Match(title="tastytrade"),        # tastytrade pop-out side gutter
        Match(title="tastytrade - Portfolio Report"), # tastytrade pop-out allocation
        Match(wm_class="tasty.javafx.launcher.LauncherFxApp"), # tastytrade settings
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
   home = os.path.expanduser('~')
   subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
