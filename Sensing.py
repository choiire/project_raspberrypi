import RPi.GPIO as GPIO
import time, pickle, RPi_I2C_driver, json
import numpy as np

mylcd = RPi_I2C_driver.lcd(0x3f)

sensor_data = {"vol": "25", "sonic": "20", "qr":"00", "husky":"", "lift":"0", "box":"10"}
"""
Data = "00"
with open('qr.pickle', 'wb') as f:
    pickle.dump(Data, f)"""
#with open('lift.pickle', 'wb') as f:
#    pickle.dump(0, f)
#sonic
TRIG = 21
ECHO = 20
maxTime = 0.06

#port init
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#sonic
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

while 1:
    sonic()
    time.sleep(0.1)
    try:
        with open('/home/pi/Desktop/FINAL/status.pickle', 'rb') as f:
            status = pickle.load(f)
            sensor_data['lift'] = status["lift"]
            sensor_data['box'] = status["box"]
        with open('/home/pi/Desktop/FINAL/sensor.pickle', 'wb') as f:
            pickle.dump(sensor_data, f)
    except EOFError:
            pass
        
    #print(sensor_data)