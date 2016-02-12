#!/bin/sh

cd ~
git clone https://github.com/mrichardson23/RPi_8x8GridDraw.git
cd RPi_8x8GridDraw
mv Sense\ HAT\ Grid\ Editor.desktop ~/Desktop
sudo mv /usr/share/icons/Adwaita/ /usr/share/icons/Adwaita.fix
echo "Sense HAT Grid Editor installed. Double click the icon on the desktop to launch\n.You may now close this terminal window."
