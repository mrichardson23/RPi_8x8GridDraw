# 8x8GridDraw

This is based on https://github.com/topshed/RPi_8x8GridDraw but modified to be used as a drop-in activity. To install: 

## Installation

You can clone is repo and run it manually. Alternatively, you can open the Terminal and run these commands which does a few things to make setting up Raspberry Pi workstations a little easier:

    cd ~
    curl -L bit.ly/1PQeM7a | sh

The full details about this activity can be found here: https://dl.dropboxusercontent.com/u/48482/Sense-Hat-Activity-Plan.pdf

## Notes

Flickering cursor issues? Try this and reboot:

        sudo mv /usr/share/icons/Adwaita/ /usr/share/icons/Adwaita.fix
