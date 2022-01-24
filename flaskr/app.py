from flask import Flask,jsonify,request


import json
from transmitter import *
from myworker import celery
from dbconnection import getSqlConnection,executeQuery



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
    image_id = getImgFromStr(data["image"])
    # do database work
    query = """select * from images"""
    executeQuery(query)
    print("database work done")
    # do yolo work
    celery.send_task(
        "yolowork", args = [image_id]
    )
    print("send yolo task done")
    # do image process work
    print("send img process task done")
    return "hi"



@app.route("/getConnection")
def index():
    return "hi"

