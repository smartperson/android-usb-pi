#!/usr/bin/env python
import os
import usb.core
import time
import sys
import logging

#os.environ['PYUSB_DEBUG_LEVEL'] = 'debug'
#os.environ['PYUSB_DEBUG'] = 'debug'
#os.environ['LIBUSB_DEBUG'] = '3'
os.environ['PYUSB_LOG_FILENAME'] = os.path.abspath('~/android-usb-pi/logs/android-usb.log')


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler(os.path.abspath('~/android-usb-pi/logs/android-usb.log'))
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

logger.info('Starting USB Android audio.')

dev = usb.core.find(idVendor=int(sys.argv[1], 16), idProduct=int(sys.argv[2], 16))
mesg = dev.ctrl_transfer(0xc0, 51, 0, 0, 2)
# here we should check if it returned version 2
logger.info('received mesg of %s', mesg)
time.sleep(1)
# requesting audio
dev.ctrl_transfer(0x40, 0x3a, 1, 0, "")
logger.info('requested audio')

# putting device in accessory mode
dev.ctrl_transfer(0x40, 53, 0, 0, "")
logger.info('put into accessory mode')

logger.info('Finished USB Android audio')
