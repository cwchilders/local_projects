#!/bin/bash

# Define the absolute path to your new slideshow XML file
SLIDESHOW_PATH='file:///home/bill/Personal/Real Estate/Santa Fe/Lot 6 Private Drive 1613B Medanales/102LEICA/slideshow.xml'

# 1. Change to a temporary wallpaper to force a refresh
# Using the default Adwaita wallpaper for a quick swap
gsettings set org.gnome.desktop.background picture-uri 'file:///usr/share/backgrounds/gnome/adwaita-d.jpg'
gsettings set org.gnome.desktop.background picture-uri-dark 'file:///usr/share/backgrounds/gnome/adwaita-d.jpg'

# Wait a moment
sleep 1

# 2. Re-apply your slideshow XML
gsettings set org.gnome.desktop.background picture-uri "$SLIDESHOW_PATH"
gsettings set org.gnome.desktop.background picture-uri-dark "$SLIDESHOW_PATH"

echo "Slideshow refreshed and set to: $SLIDESHOW_PATH"