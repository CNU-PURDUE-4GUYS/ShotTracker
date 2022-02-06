import json
from transmitter import *
from myworker import celery

import asyncio

import websockets

async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        command = event["command"]
        user_id = event["user_id"]

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
        elif command == "showmeyou":
                result = celery.send_task(
                    "hello"
                )
                print(result.get())



async def main():
    async with websockets.serve(handler, "", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

# # get recent 20 history of user
# @app.route("/getUserHistory")
# def getUserHistory():
#     user = request.args.get('userid',default = "",type = str)
#     result = celery.send_task(
#         "getUserHistory" , args = [user]
#     )
#     return result

# # get recent image of user
# @app.route("/getUserImage")
# def getUserImage():
#     userid = request.args.get('userid',default = "",type = str)
#     setid = request.args.get('setid',default = "",type = str)
#     result = celery.send_task(
#         "getUserImage" , args = [userid,setid]
#     )
#     imgid = result.get()["imgid"]
#     # TODO 파이에 있는 코드 가져다가 쓰기.
#     return result


# # get image from json request and save it
# @app.route("/upload",methods=["POST"])
# def uploadImage():
#     # make and save image from request
#     data = request.get_json()
#     user_id = data["user_id"]
#     set_id = data["set_id"]
#     camera_id = data["camera_id"]
#     image_id = getImgFromStr(data["image"])
#     json_data = jsonify({
#         "user_id":user_id,
#         "camera_id":camera_id,
#         "set_id":set_id,
#         "img_id":image_id
#     })
#     # do database work
#     print("database work done")
#     celery.send_task(
#         "insertImage", args =[user_id,camera_id,set_id,image_id]
#     )
#     # do yolo work
#     celery.send_task(
#         "bulletdetection", args = [user_id,camera_id,set_id,image_id]
#     )
#     print("send yolo task done")
#     # do image process work
#     celery.send_task(
#         "targetdetection", args = [user_id,camera_id,set_id,image_id]
#     )
#     return "connection ok"




# @app.route("/showmeyou")
# def index():
    # result = celery.send_task(
    #     "hello"
    # )
    # return result.get()

