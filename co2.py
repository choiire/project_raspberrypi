'''
import serial, time

SERIAL_PORT = "/dev/serial0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout = 1)
def get_co2():
	command = [0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x00,0x79]
	ser.write(bytearray(command))
	
	response = ser.read(9)
	if len(response) == 9:
		co2_concentration = response[2]*256 + response[3]
		print(f"co2 concentration : {co2_concentration}ppm")
	else:
		print("xx")
	
if __name__ == "__main__":
	try:
		while 1:
			get_co2()
			time.sleep(2)
	except KeyboardInterrupt:
		print("guit")
		ser.close()
'''


# -*- coding: utf-8 -*-
# original: https://raw.githubusercontent.com/UedaTakeyuki/slider/master/mh_z19.py
#
# © Takeyuki UEDA 2015 -

import serial
import time
import subprocess
import traceback
import getrpimodel
import struct
import platform
import argparse
import sys
import json
import os.path

#import RPi.GPIO as GPIO
from gpiozero import Button

# setting
version = "3.1.6"
pimodel        = getrpimodel.model()
pimodel_strict = getrpimodel.model_strict()
retry_count    = 3

# exception
class GPIO_Edge_Timeout(Exception):
  pass

partial_serial_dev = 'serial0'

serial_dev = '/dev/%s' % partial_serial_dev
#stop_getty = 'sudo systemctl stop serial-getty@%s.service' % partial_serial_dev
#start_getty = 'sudo systemctl start serial-getty@%s.service' % partial_serial_dev

# major version of running python
p_ver = platform.python_version_tuple()[0]

def start_getty():
  start_getty = ['sudo', 'systemctl', 'start', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(start_getty)

def stop_getty():
  stop_getty = ['sudo', 'systemctl', 'stop', 'serial-getty@%s.service' % partial_serial_dev]
  p = subprocess.call(stop_getty)

def set_serialdevice(serialdevicename):
  global serial_dev
  serial_dev = serialdevicename

def connect_serial():
  return serial.Serial(serial_dev,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)

def read_concentration():
  try:
    ser = connect_serial()
    for retry in range(retry_count):
      result=ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      s=ser.read(9)

      if p_ver == '2':
        if len(s) >= 4 and s[0] == "\xff" and s[1] == "\x86" and checksum(s[1:-1]) == s[-1]:
          return ord(s[2])*256 + ord(s[3])
      else:
        if len(s) >= 4 and s[0] == 0xff and s[1] == 0x86 and ord(checksum(s[1:-1])) == s[-1]:
          return s[2]*256 + s[3]
  except:
     traceback.print_exc()
  return ""

def mh_z19():
  co2 = read_concentration()
  if not co2:
    return {}
  else:
    return {'co2': co2}
    
if __name__ == '__main__':
	while 1:
		mh_z19()
		time.sleep(2)
