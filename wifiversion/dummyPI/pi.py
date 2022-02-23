import os
import base64
import json
import uuid
import asyncio
import websockets

from utils import *
# python file for "dummy raspberry pi." It sends fixed "refer.jpg" and "image.jpg". REAL raspberry pi file is different from this one.
async def pihandler():
    # Sets WebSockets URI and other variables
    uri = "ws://localhost:8888"
    set_id = ""
    user_id = "jisoo"
    pi_id = "jisoopi1"
    # Connects to Websocket server
    async with websockets.connect(uri) as websocket:
        # send Hello to Websocket server.
        hello = json.dumps({
                "command":"init",
                "user_id":user_id,
                "pi_id":pi_id
        })
        await websocket.send(hello)

        async for message in websocket:
                event = json.loads(message)
                command = event["command"]
                # when receives newset, set "set_id"
                if command == "newSet":
                        set_id = event["set_id"]
                elif command == "takeRef":
                # when receivs "takeRef", take ref and send result.
                        # take reference
                        # then upload
                        result = refer_json(user_id,pi_id,set_id)
                        print(len(result))
                        await websocket.send(result)
                elif command == "takePhoto":
                        # when receivs "takePhoto", take photo and send result.
                        # take photo
                        # then upload
                        await websocket.send(image_json(user_id,pi_id,set_id))

                print(f"received {message}")


if __name__ == "__main__":
    asyncio.run(pihandler())


