import json, time, requests, asyncio, uvloop, aiohttp, pickle
from flask import Flask, json, jsonify, request, abort, make_response, render_template
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app_url = 'https://smartporter.herokuapp.com/'

async def sensors_post():
    async with aiohttp.ClientSession() as session:
        with open('/home/pi/Desktop/FINAL/sensor.pickle', 'rb') as f:
            try:
                sensor_data = pickle.load(f)
            except EOFError:
                pass
        #센서값 전송
        try:
            async with session.post((app_url+'post'), json=json.dumps(sensor_data)) as resp:
                #print(resp.status)
                pass
        except UnboundLocalError:
            pass
        #서버로부터 경로값 수신            
        async with session.get(app_url+'qrroute') as resp:
            route = json.loads(await resp.text())
            with open('/home/pi/Desktop/FINAL/GETroute.pickle', 'wb') as f:
                pickle.dump(route, f)
            time.sleep(0.1)
        #서버로부터 짐을 들것인지 정보 수신
        async with session.get(app_url+'qractuator') as resp:
            actuator = json.loads(await resp.text())
            with open('/home/pi/Desktop/FINAL/GETactuator.pickle', 'wb') as f:
                pickle.dump(actuator, f)
            time.sleep(0.1)
while 1:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sensors_post())
    loop.close
    time.sleep(0.1)