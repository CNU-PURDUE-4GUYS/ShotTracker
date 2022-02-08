import json
from transmitter import *
from myworker import celery

import asyncio

import websockets


CONNECTEDUSER = {}
CONNECTEDPI = {}


async def hellohandler(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)

async def userhandler(websocket,user_id):
    CONNECTEDUSER[user_id] = websocket
    try:
        async for message in websocket:
            event = json.loads(message)
            command = event["command"]
            
            if command == "showmeyou":
                result = celery.send_task(
                    "hello"
                )
                await websocket.send(result.get())
            
            elif command == "getUserHistory":
                result = celery.send_task(
                    "getUserHistory" , args = [user_id]
                )
                await websocket.send(result.get())
            
            elif command == "getUserImage":
                set_id = event["set_id"]
                result = celery.send_task(
                    "getUserImage" , args = [user_id,set_id]
                )
                imgid = result.get()["imgid"]
                await websocket.send(sendImageAsJson(imgid))
    finally:
        del CONNECTEDUSER[user_id]


async def pihandler(websocket,pi_id,user_id):
    CONNECTEDPI[pi_id] = websocket
    try:
        async for message in websocket:
            event = json.loads(message)
            command = event["command"]

            if command == "post_image":
                set_id = event["set_id"]
                camera_id = event["camera_id"]
                image_id = getImgFromStr(event["image"])
                print("database work done")
                
                celery.send_task(
                    "insertImage", args =[user_id,camera_id,set_id,image_id]
                )
        # do yolo work
                celery.send_task(
                    "bulletdetection", args = [user_id,camera_id,set_id,image_id]
                )
                print("send yolo task done")
        # do image process work
                celery.send_task(
                    "targetdetection", args = [user_id,camera_id,set_id,image_id]
                )
                await websocket.send("hihihihi")
            
            elif command == "showmeyou":
                result = celery.send_task(
                    "hello"
                )
                await websocket.send(result.get())
            elif command == "detectthis":
                result = celery.send_task(
                    "bulletdetection",args = [event["img_id"]]
                )
                await websocket.send("detectThisDone")
            else:
                await websocket.send("wrong command here")
            

    finally:
        del CONNECTEDPI[pi_id]




async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"
    if "user_id" in event and "pi_id" not in event:
        await userhandler(websocket,event["user_id"])
    elif "pi_id" in event:
        await pihandler(websocket,event["pi_id"],event["user_id"])
    else:
        await hellohandler(websocket)
    


async def main():
    async with websockets.serve(handler, "", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())



