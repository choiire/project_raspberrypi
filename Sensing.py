import RPi.GPIO as GPIO
import time, pickle, json, sys, subprocess, requests
import numpy as np

sensor_data = {"sonic": "20", "fire":"0", "co2":""}

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

def fire():

    sensor_data["fire"] = 0

def co2():

    sensor_data["co2"] = 0

def RunSendpy():
    Send_cmd = "/home/pi/SEND.py"
    Send_cmd_reculsive = [sys.executable, Send_cmd, '-u', 'python3']
    global pS
    pS = subprocess.Popen(Send_cmd_reculsive)  # , stdout=subprocess.PIPE, universal_newlines=True, text=True)

def RunQRpy():
    QR_cmd = "/home/pi//QR.py"
    QR_cmd_reculsive = [sys.executable, QR_cmd, '-u', 'python3']
    global pQ
    pQ = subprocess.Popen(
        QR_cmd_reculsive)  # ,stdout=subprocess.PIPE, universal_newlines=True, text=True)#, encoding='UTF-8')
    time.sleep(2)

def KillSendpy():
    pS.kill()
    pS.terminate()

def KillQRpy():
    pQ.kill()
    pQ.terminate()

if __name__ == '__main__':

    RunSendpy()  # 통신 시작
    RunQRpy()
    while 1:

        sonic()
        time.sleep(0.1)
        fire()
        time.sleep(0.1)
        co2()
        time.sleep(0.1)

        try:
            with open('/home/pi/sensor.pickle', 'wb') as f:
                pickle.dump(sensor_data, f)
        except EOFError:
            pass

    KillSendpy()
    KillQRpy()
