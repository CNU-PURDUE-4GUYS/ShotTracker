import os
import base64
import json
import uuid
import asyncio
import websockets

from utils import *

async def pihandler():
    # 파이는 켜지면 웹소켓 서버와 연결을 하고,
    # 세트 아이디 초기화
    uri = "ws://localhost:8888"
    set_id = ""
    user_id = "jisoo"
    pi_id = "jisoopi1"
    # 웹소켓 서버와 연결한다.
    async with websockets.connect(uri) as websocket:
        # 파이의 접속을 알린다.
        # 세트 아이디를 제공한다.
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
                        
                        # take reference
                        # then upload
                        result = refer_json(user_id,pi_id,set_id)
                        print(len(result))
                        await websocket.send(result)
                elif command == "takePhoto":
                        # take photo
                        # then upload
                        await websocket.send(image_json(user_id,pi_id,set_id))

                print(f"received {message}")


if __name__ == "__main__":
    asyncio.run(pihandler())


