import time, pickle, requests

app_url = 'https://smartporter.herokuapp.com/'
sensor_data1= requests.get(url=(app_url+'reset'))
#======================================================
status = {"pump" : "0", "solenoid" : "0", "fan" : "0"}
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
sensor_data = {"sonic": "20", "fire":"0", "co2":""}
with open('/home/pi/Desktop/FINAL/sensor.pickle', 'wb') as f:
    pickle.dump(sensor_data, f)