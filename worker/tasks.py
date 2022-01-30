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
    return executeQuery(query)


@celery.task(name="getUserHistory")
def getUserHistory(user_id):
    query = f"select * from shootingsets where userid = '{user_id}' order by startedtime ASC limit 20"
    result = executeQuery(query)
    logger.info("getUserHistorydone")
    return result


@celery.task(name="insertImage")
def insertImage(user_id,camera_id,set_id,image_id):
    now = datetime.datetime.now()
    query = f"insert into images (userid,cameraid,setid,imgid,saveddate) VALUES ('{user_id}', '{camera_id}', '{set_id}', '{image_id}','{now}')"
    doInserteQuery(query)
    logger.info("inserted image info into database")
    return

# do yolo work heres
@celery.task(name="bulletdetection")
def bulletdetection(user_id,camera_id,set_id,image_id):
    # detect = Detect_class()
    # coordinates = detect.run(img_id)
    # query = f"insert into bullets (imgid,xposition,yposition) VALUES ('{img_id}', '{coordinates[0]}', '{coordinates[1]}')"
    # doInserteQuery(query)
    # logger.info("database work done")
    # return timeline
    return

# do image process here
@celery.task(name="targetdetection")
def targetdetection(user_id,camera_id,set_id,image_id):
    print("targetdetection work")
    return
