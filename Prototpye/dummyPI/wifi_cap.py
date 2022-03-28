from capture import Picture
import os
import base64
import json
import uuid
import asyncio
import websockets

from utils import *

async def pihandler():
    # real pi
    uri = "ws://172.20.10.7:8888"
    set_id = ""
    user_id = "jisoo"
    pi_id = "jisoopi1"
    # websocket connection
    async with websockets.connect(uri) as websocket:
        # signaling
        hello = json.dumps({
                "command":"init",
                "user_id":user_id,
                "pi_id":pi_id
        })
        await websocket.send(hello)

        async for message in websocket:
                event = json.loads(message)
                command = event["command"]
                if command == "newSet":
                        set_id = event["set_id"]
                elif command == "takeRef":
                        pic = Picture(None)
                        path = "/home/pi/refer"
                        pic.takePic(path)	                       # take reference
                        # then upload
                        result = refer_json(user_id,pi_id,set_id)
                        print(len(result))
                        await websocket.send(result)
                elif command == "takePhoto":
                        pic = Picture(None)
                        path = "/home/pi/image"
                        pic.takePic(path)
                        # take photo
                        # then upload
                        await websocket.send(image_json(user_id,pi_id,set_id))

                print(f"received {message}")


if __name__ == "__main__":
    asyncio.run(pihandler())



