import time, pickle, random, json, math, smbus, sys, subprocess, requests
import RPi.GPIO as GPIO
import rpi_dc_lib

sensor_data = {"vol": "25", "sonic": "20", "qr":"00", "husky":"", "lift":"0", "box":"10"}
status = {"direction" : "4", "lift" : "0", "box" : "10"}# 동, 엑츄 off

with open('/home/pi/Desktop/FINAL/status.pickle', 'wb') as f:
    pickle.dump(status, f)

Data = "00"
with open('/home/pi/Desktop/FINAL/qr.pickle', 'wb') as f:
    pickle.dump(Data, f)

route1 = ['00'] #초기값
app_url = 'https://smartporter.herokuapp.com/'
route = []
server_route = []

#relay
relay_1 = 12
relay_2 = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_1,GPIO.OUT)
GPIO.setup(relay_2,GPIO.OUT)

GPIO.output(relay_1,0)
GPIO.output(relay_2,0)

def RunSendpy():
    Send_cmd = "/home/pi/Desktop/FINAL/Communication.py"
    Send_cmd_reculsive = [sys.executable, Send_cmd, '-u', 'python3']
    global pS
    pS = subprocess.Popen(Send_cmd_reculsive)#, stdout=subprocess.PIPE, universal_newlines=True, text=True)
    
def RunSensingpy():
    Sensor_cmd = "/home/pi/Desktop/FINAL/Sensing.py"
    Sensor_cmd_reculsive = [sys.executable, Sensor_cmd, '-u', 'python3']  
    global pSS
    pSS = subprocess.Popen(Sensor_cmd_reculsive)#, stdout=subprocess.PIPE, universal_newlines=True, text=True)

def RunQRpy():
    QR_cmd = "/home/pi/Desktop/FINAL/QR.py"
    QR_cmd_reculsive = [sys.executable, QR_cmd, '-u', 'python3']
    global pQ
    pQ = subprocess.Popen(QR_cmd_reculsive)#,stdout=subprocess.PIPE, universal_newlines=True, text=True)#, encoding='UTF-8')
    time.sleep(2)

def KillSendpy():
    pS.kill()
    pS.terminate()

def KillSensingpy():
    pSS.kill()
    pSS.terminate()

def KillQRpy():
    pQ.kill()
    pQ.terminate()
    
def Actuator(a):
    # 작동 지시를 받고 작동
    if a == 0: #Down
        GPIO.output(relay_1,0)
        GPIO.output(relay_2,0)
        
    elif a == 1: #Up
        GPIO.output(relay_1,1)
        GPIO.output(relay_2,1)
        
    time.sleep(8.5)# 작동 완료 시간
    status["lift"] = a # 값변경
    
def setactuator():
    # 엑츄 작동값 서버에서 받기
    try:
        with open('/home/pi/Desktop/FINAL/GETactuator.pickle', 'rb') as f:
            actuator = pickle.load(f)
    except EOFError:
        actuator = "0"
    
    #작동
    if (actuator == "0") and (int(status["lift"]) == 1):
        #리프트가 올라가져 있고, 서버에서는 내리라고 했을때
        #리프트를 내린후 박스 위치값 저장
        Actuator(0)
        status["box"] = route[0]
    elif (actuator == "1") and (int(status["lift"]) == 0):
        #리프트가 내려가져 있고, 서버에서는 올리라고 했을때
        #리프트를 올린후 박스 떠있음 서버 전송
        Actuator(1)
        status["box"] = route[0]#"44"
    
    with open('/home/pi/Desktop/FINAL/status.pickle', 'wb') as f:
        pickle.dump(status, f)

def Getweb():
    # 서버 경로값을 저장하는 파일이 별도로 있지만
    # pickle 파일은 열때 오류가 생길 위험 때문에 별도로 서버에서 수신
    try:
        sensor_data1= requests.get(url=(app_url+'qrroute'))    
        data = json.loads(sensor_data1.json())
        if data != "[]":
            return data
            #return data[1:]
        else:
            return "[]"
    except requests.exceptions.ConnectionError:
        Getweb()
def Getroute():
    global route
    global route1
    global server_route
    global get_route
    get_route = Getweb()
    #print(get_route)
    #print(11111111111111111111111111111111)
    if (get_route != server_route) and ((type(get_route) is list)==0):
        # 초기 저장한 서버루트와 현 서버루트가 보기에 같지만
        # 타입 차이로 인해 에러가 날때
        #한 마디로 처음 시작했을때 다음 서버경로를 받을 때까지 기다리는 곳
        #Pause()
        while (type(get_route) is list)==0:
            time.sleep(1)
            Mbrake()
            get_route = Getweb()
            #print(get_route)
            #print(6666666666)
            #print(route)
            #print(server_route)
            if (type(get_route) is list)==1:
                break
                #Getroute()
    elif (get_route != server_route) and ((type(get_route) is list)==1):
        #받아둔 서버루트와 지금 서버루트가 같지 않을때
        # + 서버루트가 빈 항목이 아닐때
        # 받아둔 서버루트를 현 서버루트로 갱신
        server_route = get_route
        route = route1 + server_route
    elif (get_route == server_route) and (len(route)==1):
        #받아둔 서버루트와 현 서버루트가 같을때
        # + 더이상 이동할 경로가 없을때
        while get_route == server_route:
            time.sleep(1)
            Mbrake()
            get_route = Getweb()
            route1 = route
            if (get_route != server_route):
                server_route = get_route
                route = route1 + server_route
            if len(route)!=1:
                break

def Turn(side):
    Gyro_cmd = "/home/pi/Desktop/FINAL/Gyro.py"
    Gyro_cmd_reculsive = [sys.executable, Gyro_cmd, '-u', 'python3']  
    p = subprocess.Popen(Gyro_cmd_reculsive,stdout=subprocess.PIPE, universal_newlines=True, text=True)
    time.sleep(1)
    if int(status["lift"]) == 0:
        SS = 20
    elif int(status["lift"]) == 1:
        SS = 20
    if side == 0:#right pi/2
        while 1:    
            pp=int(p.stdout.readline())
            if pp > 880:
                Mbrake()
                break
            #Rturn()
            RRturn(SS)
            time.sleep(0.001)
    elif side == 1:#left pi/2
        while 1:    
            pp=int(p.stdout.readline())
            if pp < -880:
                Mbrake()
                break
            #Lturn()
            LLturn(SS)
            time.sleep(0.001)
    elif side == 2:#right pi
        while 1:    
            pp=int(p.stdout.readline())
            if pp > 1748:
                Mbrake()
                break
            #Rturn()
            RRturn(SS)
            time.sleep(0.001)
    elif side == 3:#left pi
        while 1:    
            pp=int(p.stdout.readline())
            if pp < -1748:
                Mbrake()
                break
            #Lturn()
            LLturn(SS)
            time.sleep(0.001)
    else:
        pass
    
    p.terminate()
    p.kill()
    
def Arrow():#[(A,B), (C,D)] 좌표비교
    # route 0,1번째 좌표비교해서 방향 결정
    global route
    A = 0
    B = 1
    C = 0
    D = 1
    try:
        if ((int(route[0]) == int(route[1]) and (len(route) != 1))):
            del route[0]
        if int(route[0][B]) < int(route[1][D]): #B < D 비교
            return 1 #동
        elif int(route[0][B]) > int(route[1][D]): #B > D 비교
            return 2 #서
        elif int(route[0][B]) == int(route[1][D]): 
            if int(route[0][A]) > int(route[1][C]): #A < C 비교
                return 3 #남
            elif int(route[0][A]) < int(route[1][C]): #A > C 비교
                return 4 #북
        else:# 오류. 아마 route가 꼬여서 그런걸수도...?
            time.sleep(0.1)
            Arrow()
    except IndexError:
        return 0

def Decideway():
    # 현재 방향과 다음 좌표와의 방향을 비교해서
    # 그에맞는 방향으로 움직임
    way = int(Arrow())
    di = int(status["direction"])
    if di != way:
        if (((di == 1) and (way == 4)) or ((di == 4) and (way == 2)) or ((di == 2) and (way == 3)) or ((di == 3) and (way == 1))):
            Turn(0)#turn right pi/2
        elif (((di == 1) and (way == 3)) or ((di == 3) and (way == 2)) or ((di == 2) and (way == 4)) or ((di == 4) and (way == 1))):
            Turn(1)#turn left pi/2
        elif (((di == 1) and (way == 2)) or ((di == 2) and (way == 1)) or ((di == 3) and (way == 4)) or ((di == 4) and (way == 3))):
            Turn(2)#turn right pi
        if way != 0:
            status["direction"] = int(way)
    else:
        pass

def Husky(SS):
    try:
        with open('/home/pi/Desktop/FINAL/husky.pickle', 'rb') as f:
            husky = pickle.load(f)
            x = int(husky["x"])
            y = int(husky["y"])
            #Xoffset = 160-155
            xx = x #+ Xoffset
            if y <= 120:
                if (xx > 175):#179
                    MotorL.forward(SS+9)
                    time.sleep(0.00005)
                    #time.sleep(0.005)
                    #time.sleep(0.00015)
                elif (xx < 145):#138
                    MotorR.forward(SS+9)
                    time.sleep(0.00005)
                    #time.sleep(0.00015)
                    #time.sleep(0.005)
            elif y > 120:
                if (xx > 182):#179
                    MotorL.forward(SS+9)
                    #time.sleep(0.00015)
                    time.sleep(0.00005)
                elif (xx < 138):#138
                    MotorR.forward(SS+9)
                    time.sleep(0.00005)
                    #time.sleep(0.00015)
    except EOFError:
        pass
    except ValueError:
        pass
    
def Goforward(QR):
    time.sleep(0.1)
    RunHuskypy()
    #M1forward()
    if int(status["lift"]) == 0:
        #Mforward()
        #MMforward(12)
        SS = 15
    elif int(status["lift"]) == 1:
        #MMforward(16)
        SS = 18
    while 1:
        ######전진
        Husky(SS)
        MMforward(SS)
        
        try:
            with open('/home/pi/Desktop/FINAL/qr.pickle', 'rb') as f:
                if (int(pickle.load(f)) == int(QR)):
                    time.sleep(0.01)
                    break
            with open('/home/pi/Desktop/FINAL/sensor.pickle', 'rb') as f:
                sensor_data = pickle.load(f)
        except EOFError:
            sensor_data["sonic"] = 100
            pass
        
        ######초음파
        while int(sensor_data["sonic"]) < 10:
            try:
                with open('/home/pi/Desktop/FINAL/sensor.pickle', 'rb') as f:
                    sensor_data = pickle.load(f)
            except EOFError:
                pass
            Mbrake()
            time.sleep(0.001)
    ######################################
    Mbrake()
    KillHuskypy()

#####################################################


if __name__ == '__main__':
    
    MotorL = rpi_dc_lib.L298NMDc(13 ,6 ,17 ,130 ,True, "motor_one")
    MotorR = rpi_dc_lib.L298NMDc(26 ,19 ,27 ,130 ,True, "motor_two")
    
    RunSendpy()#통신 시작
    RunSensingpy()
    RunQRpy()
    while 1:
        Getroute()#루트 갱신
        Decideway()#갈 방향을 결정
        try:
            Goforward(route[1])#앞 경로까지 감
            del route[0]
            
            if (len(route)==1):
                setactuator()#엑츄에이터 작동
            time.sleep(0.001)
        except IndexError:#다 도착해서 갈 곳이 없을때
            if (len(route)==1):
                setactuator()#엑츄에이터 작동
            Getroute()#다시 루트 갱신
            time.sleep(0.001)
            
    KillSendpy()
    KillSensingpy() 