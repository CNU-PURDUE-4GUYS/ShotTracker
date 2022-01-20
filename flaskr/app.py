from flask import Flask,jsonify,request
import mysql.connector
import uuid
import json
import base64
from io import BytesIO
# make Connection to MySQL
def getSqlConnection():
    config = {
        "user": "root",
        "host": "db",
        "port": "3306",
        "password": "pass",
        "database": "mytest",
        "auth_plugin": "mysql_native_password",
}
    connection = mysql.connector.connect(**config)
    return connection


app = Flask(__name__)




# receive and save image from JSON Request
def getImgFromJsonRequest(request):
    dict_data = request.get_json() #Get the POSTed json
    img = dict_data["img"] #Take out base64# str
    #print(img)
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img)
    img.save(str(uuid.uuid4())+".jpg")
    img_shape = img.size #Appropriately process the acquired image
    text = dict_data["name"] + "fuga" #Properly process with the acquired text
    response = {
        "name":text,
        "img_shape":img_shape
        }
    return jsonify(response)


@app.route("/upload",methods=["GET","POST"])
def hello_world():
    # res = getImgFromJsonRequest(request)
    return "hello world"


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
    return "Nice to see you"
