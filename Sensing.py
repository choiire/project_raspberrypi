import RPi.GPIO as GPIO
import time, pickle,serial, subprocess,traceback, getrpimodel, struct, platform, argparse, sys, json,os.path
import numpy as np
from gpiozero import Button

sensor_data = {"sonic": "20", "fire":"0", "co2":""}

#fire
fire_pin = 16

#sonic
TRIG = 21
ECHO = 20
maxTime = 0.06

#port init
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(fire_pin, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def sonic():
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while ((GPIO.input(ECHO) == 0) and (pulse_start < timeout)):
        pulse_start = time.time()
        
    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while ((GPIO.input(ECHO) == 1) and (pulse_end < timeout)):
        pulse_end = time.time()
        
    duration = pulse_end - pulse_start
    distance = int(duration * 17000)
    sensor_data["sonic"] = distance
    print(distance)

# setting
version = "3.1.6"
pimodel        = getrpimodel.model()
pimodel_strict = getrpimodel.model_strict()
retry_count    = 3

# exception
class GPIO_Edge_Timeout(Exception):
  pass

partial_serial_dev = 'ttyAMA0'

serial_dev = '/dev/%s' % partial_serial_dev
p_ver = platform.python_version_tuple()[0]

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

def checksum(array):
  if p_ver == '2' and isinstance(array, str):
    array = [ord(c) for c in array]
  csum = sum(array) % 0x100
  if csum == 0:
    return struct.pack('B', 0)
  else:
    return struct.pack('B', 0xff - csum + 1)

def cal():
  ser = connect_serial()
  for retry in range(retry_count):
    result=ser.write(b"\xff\x01\x87\x00\x00\x00\x00\x00\x78")

def cal_expand():
  ser = connect_serial()
  for retry in range(retry_count):
    result=ser.write(b"\xff\x01\x88\x07\xD0\x00\x00\x00\xA0")

if __name__ == '__main__':
    cal()
    cal_expand()
    while 1:
        sonic()
        time.sleep(0.1)
        fire = GPIO.input(fire_pin)
        sensor_data["fire"] = fire
        sensor_data["co2"] = read_concentration()
        
        try:
            with open('/home/pi/Desktop/FINAL/sensor.pickle', 'wb') as f:
                pickle.dump(sensor_data, f)
        except EOFError:
                pass
            
        print(sensor_data)
