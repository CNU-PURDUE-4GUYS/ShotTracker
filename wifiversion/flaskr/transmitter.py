from flask import request
import uuid
import base64
from io import BytesIO
import os
from PIL import Image
import json
# This is module for making JSON Message.


# receive and save image from JSON Request
def getImgFromStr(image):
    img = image #Take out base64# str
    #print(img)
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img)
    img_id = str(uuid.uuid4())
    img.save("/app/images/"+img_id+".jpg")
    # img_shape = img.size #Appropriately process the acquired image
    return img_id
# receive and save image from JSON Request
def getRefFromStr(image):
    img = image #Take out base64# str
    #print(img)
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img)
    img_id = str(uuid.uuid4())
    img.save("/app/refs/"+img_id+".jpg")
    # img_shape = img.size #Appropriately process the acquired image
    return img_id

# find warped image in warps folder and make json message

def sendWarpAsJson(img_id,user_id = "jisoo",set_id="1",bullets=None):
    image = "/app/warps/"+img_id +".jpg"
    with open(image,"rb") as image_file:
        image_read = base64.b64encode(image_file.read()).decode("utf-8")
        body = {
            "command":"warp",
            "user_id":user_id,
            "set_id":set_id,
            "image":image_read,
            "bullets":bullets
            }
        return json.dumps(body)

# find image in images folder and make json message

def sendImageAsJson(img_id,user_id = "jisoo",set_id="1"):
    image = "/app/images/"+img_id +".jpg"
    with open(image,"rb") as image_file:
        image_read = base64.b64encode(image_file.read()).decode("utf-8")
        body = {
            "command":"photo",
            "user_id":user_id,
            "set_id":set_id,
            "image":image_read
            }
        return json.dumps(body)

# find refer in ref folder and make json message
def sendReferAsJson(img_id,user_id = "jisoo",set_id="1"):
    image = "/app/refs/"+img_id +".jpg"
    with open(image,"rb") as image_file:
        image_read = base64.b64encode(image_file.read()).decode("utf-8")
        body = {
            "command":"refer",
            "user_id":user_id,
            "set_id":set_id,
            "image":image_read
            }
        return json.dumps(body)
# newSetMessageToPi&Client
def newSetMessage(user_id,set_id):
    body = {
        "command":"newSet",
        "user_id":user_id,
        "set_id":set_id
        }
    return json.dumps(body)

# refer message to raspberry pi "takeRefer"
def takeRefMessage(user_id,set_id):
    body = {
        "command":"takeRef",
        "user_id":user_id,
        "set_id":set_id
        }
    return json.dumps(body)

# photo message to raspberry pi "takePhoto"
def takePhotoMessage(user_id,set_id):
    body = {
        "command":"takePhoto",
        "user_id":user_id,
        "set_id":set_id
        }
    return json.dumps(body)