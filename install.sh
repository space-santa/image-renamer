#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

sudo dnf install -y python3-exif

sudo cp ReNamer.py /usr/local/bin/jpg-renamer
sudo cp jpg-renamer.png /usr/share/icons/hicolor/64x64/apps/jpg-renamer.png
sudo cp jpg-renamer.desktop /usr/share/applications/jpg-renamer.desktop
sudo cp jpg-renamer-service.desktop /usr/share/kde4/services/ServiceMenus/jpg-renamer-service.desktop
sudo cp jpg-renamer-service.desktop /usr/share/kservices5/ServiceMenus/jpg-renamer-service.desktop