#!/usr/bin/env python
import os
import usb.core
import time
import sys
import logging

#os.environ['PYUSB_DEBUG_LEVEL'] = 'debug'
#os.environ['PYUSB_DEBUG'] = 'debug'
#os.environ['LIBUSB_DEBUG'] = '3'
#os.environ['PYUSB_LOG_FILENAME'] = '/home/pi/android-usb.log'

def send_command(dev_handle, command):
    dev_handle.ctrl_transfer(0x40, 57, 0x01, 0, command)
    #dev_handle.ctrl_transfer(0x40, 57, 0x01, 0, '\x00')

def send_playpause(dev_handle):
    send_command(dev_handle, '\x08')
def send_prevtrack(dev_handle):
    send_command(dev_handle, '\x20')
def send_nexttrack(dev_handle):
    send_command(dev_handle, '\x10')

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create a file handler
    handler = logging.FileHandler('/home/pi/android-usb.log')
    handler.setLevel(logging.DEBUG)
    
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(handler)
    
    logger.info('Starting USB Android control.')
    # Once accessory mode is active we will communicate over the AOA 2.0 product ID instead of the original product ID
    dev = usb.core.find(idVendor=0x18d1, idProduct=0x2d02)
    # let's try registering an HID device!
    descriptor_data = [    0x05, 0x0c,
        0x05, 0x0c,                    # USAGE_PAGE (Consumer Devices)
        0x09, 0x01,                    #   USAGE (Consumer Control)
        0xa1, 0x01,                    # COLLECTION (Application)
        0x05, 0x0c,                    #   USAGE_PAGE (Consumer Devices)
        0x15, 0x00,                    #   LOGICAL_MINIMUM (0)
        0x25, 0x01,                    #   LOGICAL_MAXIMUM (1)
        0x09, 0xb0,                    #   USAGE (Play)
        0x09, 0xb1,                    #   USAGE (Pause)
        0x09, 0xb7,                    #   USAGE (Stop)
        0x09, 0xcd,                    #   USAGE (play/pause)
        0x09, 0xb5,                    #   USAGE (Scan Next Track)
        0x09, 0xb6,                    #   USAGE (Scan Previous Track)
        0x09, 0xb4,                    #   USAGE (Rewind)
        0x09, 0xb3,                    #   USAGE (Fast Forward)
        0x95, 0x08,                    #   REPORT_COUNT (8)
        0x75, 0x01,                    #   REPORT_SIZE (1)
        0x81, 0x06,                    #   INPUT (Data,Var,Rel)
        0xc0                           # END_COLLECTION
    ]
     
     
    descriptor_str = "".join(chr(n) for n in descriptor_data)
    mesg = dev.ctrl_transfer(0x40, 54, 0x01, len(descriptor_str), "")
    logger.info('set as HID device, mesg: %s', mesg)
    # now let's send the HID report descriptor
    logger.info('descriptor data is of length %d', len(descriptor_str))
    logger.info('descriptor string is: %s',descriptor_str)
    dev.ctrl_transfer(0x40, 56, 0x01, 0, descriptor_str)
    logger.info('sent HID report descriptor of length %d', len(descriptor_str))
    time.sleep(1)
    
    dev.ctrl_transfer(0x40, 57, 0x01, 0, '\x00')
    logger.info('sent 0')
        
    #send_playpause(dev)
    #send_nexttrack(dev)
    #send_prevtrack(dev)
    #send_prevtrack(dev)
    
    while True:
        in_pipe = open('/home/pi/android_control_pipe', 'r')
        c = in_pipe.read()
        if c.endswith("\n"): c = c[:-1]
        in_pipe.close()
        #sys.stdout.write(c)
        print c
        if c == "\n":
            break
        elif c == 'a':
            send_prevtrack(dev)
        elif c == 's':
            send_playpause(dev)
        elif c == 'd':
            send_nexttrack(dev)
        else:
            print 'invalid command'

main()
