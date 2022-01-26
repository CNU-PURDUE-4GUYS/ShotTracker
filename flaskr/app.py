from flask import Flask,jsonify,request
import json
from transmitter import *
from myworker import celery

app = Flask(__name__)

# hello world 
@app.route("/")
def hello_world():
    return "res"


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
        "yolowork", args = [image_id]
    )
    print("send yolo task done")
    # do image process work
    celery.send_task(
        "imageprocessing", args = [image_id]
    )
    print("send img process task done")
    return "hi"



@app.route("/getConnection")
def index():
    celery.send_task(
        "hello"
    )
    return "hi"

