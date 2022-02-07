from flask import request
import uuid
import base64
from io import BytesIO
import os
from PIL import Image
import json



# receive and save image from JSON Request
def getImgFromStr(image):
    img = image #Take out base64# str
    #print(img)
    img = base64.b64decode(img) #Convert image data converted to base64 to original binary data# bytes
    img = BytesIO(img) # _io.Converted to be handled by BytesIO pillow
    img = Image.open(img)
    img_id = str(uuid.uuid4())
    img.save("./images/"+img_id+".jpg")
    # img_shape = img.size #Appropriately process the acquired image
    response = {
        "img_id":img_id,
        }
    return img_id

# send image as json
def sendImageAsJson(img_id):
    image = img_id +".jpg"
    with open(image,"rb") as image_file:
        image_read = base64.b64encode(image_file.read()).decode("utf-8")
        body = {
            "user_id":"jisoo",
            "camera_id":"camera1",
            "set_id":"set1",
            "image":image_read
            }
        return json.dumps(event)