import time, pickle, requests

app_url = 'https://smartporter.herokuapp.com/'
sensor_data1= requests.get(url=(app_url+'reset'))
#======================================================
status = {"direction" : "4", "lift" : "0", "box" : "10"}# 남, 엑츄 off
with open('/home/pi/Desktop/FINAL/status.pickle', 'wb') as f:
    pickle.dump(status, f)

#======================================================
Data = "00"
with open('/home/pi/Desktop/FINAL/qr.pickle', 'wb') as f:
    pickle.dump(Data, f)

#======================================================
actuator = "0"
with open('/home/pi/Desktop/FINAL/GETactuator.pickle', 'wb') as f:
    pickle.dump(actuator, f)

#======================================================
route = ["00"]
with open('/home/pi/Desktop/FINAL/GETroute.pickle', 'wb') as f:
    pickle.dump(route, f)

#======================================================
HL = {"x": "", "y": ""}
with open('/home/pi/Desktop/FINAL/husky.pickle', 'wb') as f:
    pickle.dump(HL, f)

#======================================================
sensor_data = {"vol": "25", "sonic": "20", "qr":"00", "husky":"", "lift":"0", "box":"10"}
with open('/home/pi/Desktop/FINAL/sensor.pickle', 'wb') as f:
    pickle.dump(sensor_data, f)