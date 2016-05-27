# 8x8GridDraw

This is based on https://github.com/topshed/RPi_8x8GridDraw but modified to be used as a drop-in activity at events. There are two levels to this activity:

1. The point-and-click interface for creating animations on the Sense HAT's LED matrix. This is meant for some quick fun and can be used by younger participants who can't read, but can point and click with a mouse.
2. The Python command line interpreter interface for trying out the Sense HAT functions. This is meant to get people coding quickly. The shortcut installed on the desktop loads the Sense HAT module automatically and creates a SenseHat() object that's ready to use right away.

## Installation

You can clone is repo and run it manually. Alternatively, you can open the Terminal and run these commands which does a few things to make setting up Raspberry Pi workstations a little easier:

    cd ~
    curl -L bit.ly/1PQeM7a | sh

The full details about this activity can be found here: https://dl.dropboxusercontent.com/u/48482/Sense-Hat-Activity-Plan.pdf

## Notes

Flickering cursor issues? Try this and reboot:

        sudo mv /usr/share/icons/Adwaita/ /usr/share/icons/Adwaita.fix
