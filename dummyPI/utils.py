import os
import base64
import json
import uuid

# find image with "img_id",and convert into string, then return json dumped message.
def image_json(user_id,pi_id,set_id,img_id = "image"):
    image = img_id+".jpg"
    with open(image,"rb") as image_file:
        image_read = base64.b64encode(image_file.read()).decode("utf-8")
        #print(image_read)
        body = {
        "command":"photo","user_id":user_id,"pi_id":pi_id,"set_id":set_id,"image":image_read}
        return json.dumps(body)
    
# find refer image with "img_id" ,and convert into string, then return json dumped message.

def refer_json(user_id,pi_id,set_id,img_id = "refer"):
    image = img_id+".jpg"
    with open(image,"rb") as image_file:
        image_read = base64.b64encode(image_file.read()).decode("utf-8")
        #print(image_read)
        body = {
        "command":"refer","user_id":user_id,"pi_id":pi_id,"set_id":set_id,"image":image_read}
        return json.dumps(body)
