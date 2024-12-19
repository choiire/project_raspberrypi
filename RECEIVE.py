import json, time, requests, asyncio, uvloop, aiohttp, pickle
from flask import Flask, json, jsonify, request, abort, make_response, render_template
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app_url = 'https://smartporter.herokuapp.com/'

async def sensors_post():
    async with aiohttp.ClientSession() as session:
        #서버로부터 경로값 수신            
        async with session.get(app_url+'status') as resp:
            status = json.loads(await resp.text())
            with open('/home/pi/status.pickle', 'wb') as f:
                pickle.dump(status, f)
            time.sleep(0.1)
while 1:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sensors_post())
    loop.close
    time.sleep(0.1)