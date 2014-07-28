#!/bin/bash

/root/android-usb-pi/android-usb-audio.py $1 $2
(sleep 3s ; pactl load-module module-loopback source=`pactl list sources short | grep alsa_input.usb | cut -f 1`) &
/root/android-usb-pi/android-usb-control.py