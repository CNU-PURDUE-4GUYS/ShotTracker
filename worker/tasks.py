from celery import Celery
import os
from dbconnection import getSqlConnection,executeQuery,doInserteQuery
from celery.utils.log import get_task_logger
# from yolov5.detect import Detect_class
import time    
import datetime


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

logger = get_task_logger(__name__)


@celery.task(name="hello")
def hello():
    query = """select * from images"""
    logger.info(executeQuery(query))
    logger.info("database work done")
    logger.info("hello from celery!!")
    return

@celery.task(name="insertImage")
def insertImage(user_id,camera_id,set_id,image_id):
    now = datetime.datetime.now()
    logger.info(f"image id is {image_id}")
    query = f"insert into images (userid,cameraid,setid,imgid,saveddate) VALUES ('{user_id}', '{camera_id}', '{set_id}', '{image_id}','{now}')"
    doInserteQuery(query)
    logger.info("database work done")
    return

# do yolo work heres
@celery.task(name="yolowork")
def yolowork(img_id):
    # detect = Detect_class(path)
    # coordinates = detect.run()
    # print("yolo")
    # return timeline
    return

# do image process here
@celery.task(name="imageprocessing")
def imageprocessing(img_id):
    print("image process work")
    return
