#!/bin/sh

cd ~
git clone https://github.com/mrichardson23/RPi_8x8GridDraw.git
cd RPi_8x8GridDraw
mv *.desktop ~/Desktop
sudo mv /usr/share/icons/Adwaita/ /usr/share/icons/Adwaita.fix
echo "\n\nSense HAT Grid Editor installed. Double click the icon on the desktop to launch.\nYou may now close this terminal window."
