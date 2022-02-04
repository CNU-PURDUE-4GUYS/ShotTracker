from flask import Flask,jsonify,request
import json
from transmitter import *
from myworker import celery

app = Flask(__name__)

# hello world 
@app.route("/")
def hello_world():
    return "hello world"

# get recent 20 history of user
@app.route("/getUserHistory")
def getUserHistory():
    user = request.args.get('userid',default = "",type = str)
    result = celery.send_task(
        "getUserHistory" , args = [user]
    )
    return result

# get recent image of user
@app.route("/getUserImage")
def getUserImage():
    userid = request.args.get('userid',default = "",type = str)
    setid = request.args.get('setid',default = "",type = str)
    result = celery.send_task(
        "getUserImage" , args = [userid,setid]
    )
    imgid = result.get()["imgid"]
    # TODO 파이에 있는 코드 가져다가 쓰기.
    return result


# get image from json request and save it
@app.route("/upload",methods=["POST"])
def uploadImage():
    # make and save image from request
    data = request.get_json()
    user_id = data["user_id"]
    set_id = data["set_id"]
    camera_id = data["camera_id"]
    image_id = getImgFromStr(data["image"])
    json_data = jsonify({
        "user_id":user_id,
        "camera_id":camera_id,
        "set_id":set_id,
        "img_id":image_id
    })
    # do database work
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
    return "connection ok"




@app.route("/showmeyou")
def index():
    result = celery.send_task(
        "hello"
    )
    return result.get()

