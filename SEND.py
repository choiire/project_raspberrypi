import json, time, requests, asyncio, uvloop, aiohttp, pickle
from flask import Flask, json, jsonify, request, abort, make_response, render_template
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app_url = 'https://smartporter.herokuapp.com/'

async def sensors_post():
    async with aiohttp.ClientSession() as session:
        with open('/home/pi/sensor.pickle', 'rb') as f:
            try:
                sensor_data = pickle.load(f)
            except EOFError:
                pass
        try:
            async with session.post((app_url+'post'), json=json.dumps(sensor_data)) as resp:
                #print(resp.status)
                pass
        except UnboundLocalError:
            pass
            time.sleep(0.1)
while 1:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sensors_post())
    loop.close
    time.sleep(0.1)
