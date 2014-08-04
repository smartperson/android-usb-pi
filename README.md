# android-usb-pi

A collection of scripts to allow a Raspberry Pi running a Raspbian-like OS to stream audio and control media from of Android 4.x device over USB.

----
# Prerequisites
1. Raspbian-based OS
2. pulseaudio
3. pyusb

----
## Installation
# TODOs
* write proper installation instructions
* write installer script that will just do it for you
* write update instructions
* format this document more nicely

# Instructions
1. dock.rules goes into your ```/etc/udev/rules.d/```
2. create a named pipe at ```~/android-usb-pi/android_control_pipe```
3. customize your pulseaudio setup if you have to, defaults should work.

----
## Usage
# Startup
Just plug in your android device, wait a few seconds, and trying playing some audio on it.

# Operation
To control audio, send to the named pipe the following:  

* a for previous track
* s for play/pause
* d for next track
