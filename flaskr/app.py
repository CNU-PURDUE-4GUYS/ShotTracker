import json
from transmitter import *
from myworker import celery
from logicmodule import findnewbullets
import asyncio
import uuid

import websockets

# variables for mangaing connection
CONNECTEDUSER = {}
CONNECTEDPI = {}
CURRENTSET = {}

# respond for "hello message" . using for debugging
async def hellohandler(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)

# handler for user(web client)
async def userhandler(websocket,user_id):
    CONNECTEDUSER[user_id] = websocket
    try:
        async for message in websocket:
            event = json.loads(message)
            command = event["command"]
            # get everything from database
            if command == "showmeyou":
                result = celery.send_task(
                    "hello"
                )
                await websocket.send(result.get())
            # get user history
            elif command == "getUserHistory":
                result = celery.send_task(
                    "getUserHistory" , args = [user_id]
                )
                await websocket.send(result.get())
            # get all image ids belong to specific user,specific set
            elif command == "getUserImage":
                set_id = event["set_id"]
                result = celery.send_task(
                    "getUserImage" , args = [user_id,set_id]
                )
                imgid = result.get()["imgid"]
                await websocket.send(sendImageAsJson(imgid))

            # dummy.
            elif command == "getRefImage":
                ref_id = getImgFromStr(event["image"])
            
            # receive "newSet request from clinet"
            elif command == "newSetFromCli":
                set_id = str(uuid.uuid4())
                CURRENTSET[user_id] = set_id
                result = celery.send_task(
                    "newSetInit",args = [user_id,set_id]
                ).get()
                await CONNECTEDPI[user_id].send(
                    newSetMessage(user_id,set_id)
                )
                await websocket.send(newSetMessage(user_id,set_id))
            # when get takeRef message from user, send that to connected raspberry PI
            elif command == "takeRef":
                await CONNECTEDPI[user_id].send(
                    takeRefMessage(user_id,event["set_id"])
                )
            # when get takePhoto message from user, send that to connected raspberry PI

            elif command == "takePhoto":
                await CONNECTEDPI[user_id].send(
                    takePhotoMessage(user_id,event["set_id"])
                )
    finally:
        # user disconnected
        del CONNECTEDUSER[user_id]

# handler for raspberry pi
async def pihandler(websocket,pi_id,user_id):
    CONNECTEDPI[user_id] = websocket
    try:
        async for message in websocket:
            event = json.loads(message)
            command = event["command"]


            
            # get a refer from PI. store it in local and add to database, then send to connected user
            if command == "refer":
                set_id = event["set_id"]

                ref_id = getRefFromStr(event["image"])
                result = celery.send_task(
                    "postRef",args = [user_id,set_id,ref_id]
                ).get()

                await CONNECTEDUSER[user_id].send(
                    sendReferAsJson(ref_id,user_id,set_id)
                )
            # get a photo from PI. store it in local and add to database, 
            # and warp ,and detect bullets, and store them and add to database,
            # then send to connected user
            elif command == "photo":
                set_id = event["set_id"]

                img_id = getImgFromStr(event["image"])
                # get reference.          
                ref_id = celery.send_task(
                    "getReferImage",args = [set_id]
                ).get()["refid"]
                # get former detected bullets
                formerbullets = celery.send_task(
                    "getformerBullets", args = [user_id,set_id]
                ).get()
                # detect current bullets
                bullets = celery.send_task(
                    "bulletdetection", args = [img_id,ref_id]
                ).get()
                # store in local
                celery.send_task(
                    "insertImage", args =[user_id,pi_id,set_id,img_id]
                )
                # mark new bullet, and store all bullets
                for bullet in bullets:
                    new = findnewbullets(bullet,formerbullets,threshold=3)
                    if new:
                        celery.send_task(
                            "insertBullet",args = [img_id,bullet[0],bullet[1],1]
                        ).get()
                    else:
                        celery.send_task(
                            "insertBullet",args = [img_id,bullet[0],bullet[1],0]
                        ).get()
                # send to user
                await CONNECTEDUSER[user_id].send(
                    sendWarpAsJson(img_id,user_id,set_id,celery.send_task(
                        "getBullets",args = [img_id]
                    ).get())
                )
            else:
                await websocket.send("wrong command here")
            

    finally:
        # PI disconnected
        del CONNECTEDPI[user_id]



# first reconginze connection with "init" message
# and then treat user or pi
async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["command"] == "init"
    if "user_id" in event and "pi_id" not in event:
        await userhandler(websocket,event["user_id"])
    elif "pi_id" in event:
        await pihandler(websocket,event["pi_id"],event["user_id"])
    else:
        await hellohandler(websocket)
    
# run websocket server
async def main():
    async with websockets.serve(handler, "", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())



