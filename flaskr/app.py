from flask import Flask,jsonify,request



from transmitter import *
from myworker import celery
from dbconnection import getSqlConnection



app = Flask(__name__)


# hello world 
@app.route("/")
def hello_world():
    return "hello world"


# get image from json request and save it
@app.route("/upload",methods=["POST"])
def uploadImage():
    res = getImgFromJsonRequest(request)
    return res


@app.route("/")
def index():
    DB = getSqlConnection()
    cursor = DB.cursor()
    sql = """
        SELECT * from target """
    cursor.execute(sql)
    result = cursor.fetchall()
    return str(result)

@app.route("/greeting/")
def greeting():
    celery.send_task(
            "hello"
        )
    return "Nice to see you"
