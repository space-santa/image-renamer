#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

sudo rm /usr/local/bin/jpg-renamer
sudo rm /usr/share/icons/hicolor/64x64/apps/jpg-renamer.png
sudo rm /usr/share/applications/jpg-renamer.desktop
sudo rm /usr/share/kde4/services/ServiceMenus/jpg-renamer-service.desktop
sudo rm /usr/share/kservices5/ServiceMenus/jpg-renamer-service.desktop

echo "You may want to dnf remove python3-exif."