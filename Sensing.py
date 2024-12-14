import RPi.GPIO as GPIO
import time, pickle, RPi_I2C_driver, json
import numpy as np

mylcd = RPi_I2C_driver.lcd(0x3f)

sensor_data = {"vol": "25", "sonic": "20", "qr":"00", "husky":"", "lift":"0", "box":"10"}

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
    readadc(AO_pin, SPICLK, SPIMOSI, SPIMISO, SPICS)
    time.sleep(0.1)
    try:
        with open('/home/pi/Desktop/FINAL/qr.pickle', 'rb') as f:
            sensor_data['qr'] = pickle.load(f)
        with open('/home/pi/Desktop/FINAL/husky.pickle', 'rb') as f:
            sensor_data['husky'] = pickle.load(f)
        with open('/home/pi/Desktop/FINAL/status.pickle', 'rb') as f:
            status = pickle.load(f)
            sensor_data['lift'] = status["lift"]
            sensor_data['box'] = status["box"]
        with open('/home/pi/Desktop/FINAL/sensor.pickle', 'wb') as f:
            pickle.dump(sensor_data, f)
    except EOFError:
            pass
    if sensor_data["vol"] == 25:
        vol_per = "100% [###]"
    elif sensor_data["vol"] < 24:
        vol_per = " 70% [ ##]"
    elif sensor_data["vol"] < 23:
        vol_per = " 30% [  #]"
    else:
        vol_per = "ERROR"
    try:
        mylcd.lcd_display_string("Sonic: %scm     " % sensor_data["sonic"],1)
        time.sleep(0.01)
        mylcd.lcd_display_string("Vol: %s  " %  vol_per,2)
        time.sleep(0.01)
    except OSError:
        time.sleep(0.1)
        
    #print(sensor_data)
