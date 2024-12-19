import time, pickle, random, json, math, smbus, sys, subprocess, requests
import RPi.GPIO as GPIO

sensor_data = {"sonic": "20", "fire":"0", "co2":""}
status = {"pump" : "0", "solenoid" : "0", "fan" : "0"}

with open('/home/pi/status.pickle', 'wb') as f:
    pickle.dump(status, f)

app_url = 'https://smartporter.herokuapp.com/'
route = []
server_route = []

#relay
relay_1 = 12 #pump
relay_2 = 25 #solenid
relay_3 = 25 #fan

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_1,GPIO.OUT)
GPIO.setup(relay_2,GPIO.OUT)
GPIO.setup(relay_3,GPIO.OUT)

GPIO.output(relay_1,0)
GPIO.output(relay_2,0)
GPIO.output(relay_3,0)

def RunReceivepy():
    Send_cmd = "/home/pi/RECEIVE.py"
    Send_cmd_reculsive = [sys.executable, Send_cmd, '-u', 'python3']
    global pS
    pS = subprocess.Popen(Send_cmd_reculsive)#, stdout=subprocess.PIPE, universal_newlines=True, text=True)

def KillReceivepy():
    pS.kill()
    pS.terminate()
    
def Pump(a):
    if a == 0:
        GPIO.output(relay_1,0)
    elif a == 1:
        GPIO.output(relay_1,1)

    #status["pump"] = a # 값변경

def Solenoid(a):
    if a == 0:
        GPIO.output(relay_2, 0)
    elif a == 1:
        GPIO.output(relay_2, 1)

    #status["solenoid"] = a  # 값변경

def Fan(a):
    if a == 0:
        GPIO.output(relay_3, 0)
    elif a == 1:
        GPIO.output(relay_3, 1)

    #status["fan"] = a  # 값변경

def Getstatus():
    try:
        sensor_data1= requests.get(url=(app_url+'status'))
        data = json.loads(sensor_data1.json())
        if data != "[]":
            return data
            #return data[1:]
        else:
            return "[]"
    except requests.exceptions.ConnectionError:
        time.sleep(0.001)

#####################################################


if __name__ == '__main__':

    #RunReceivepy()
    while 1:
        data = Getstatus()#루트 갱신
        time.sleep(0.01)
        if (int(data["fire"]) == 1) & (int(data["sonic"]) < 10):
            Pump(1)
            time.sleep(0.01)
            Solenoid(1)
            time.sleep(0.01)
        if (int(data["co2"]) == 5000):
            Fan(1)
        time.sleep(0.01)
    #KillReceivepy()
