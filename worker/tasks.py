from celery import Celery
import os
from dbconnection import getSqlConnection,executeQuery,doInserteQuery
from celery.utils.log import get_task_logger
from yolov5.detect import Detect_class
import time    
import datetime
from alignment.align_matrix import ImageAlignment


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

logger = get_task_logger(__name__)


@celery.task(name="hello")
def hello():
    detect = Detect_class(1)
    detect.run(source='front')
    return "hello"


@celery.task(name="getUserHistory")
def getUserHistory(user_id):
    query = f"select * from shootingsets where userid = '{user_id}' order by startedtime ASC limit 20"
    result = executeQuery(query)
    logger.info("getUserHistorydone")
    return result

@celery.task(name="getUserImage")
def getUserImage(user_id,set_id):
    query = f"select imgid from images where userid = '{user_id}' and setid = '{set_id}' order by saveddate ASC limit 1"
    result = executeQuery(query)
    logger.info("getUserImage done")
    return result[0]


@celery.task(name="insertImage")
def insertImage(user_id,camera_id,set_id,image_id):
    now = datetime.datetime.now()
    query = f"insert into images (userid,cameraid,setid,imgid,saveddate) VALUES ('{user_id}', '{camera_id}', '{set_id}', '{image_id}','{now}')"
    doInserteQuery(query)
    logger.info("inserted image info into database")
    return

# do yolo work heres
@celery.task(name="bulletdetection")
def bulletdetection(image_id):
    refer_id = "ref"
    alignment = ImageAlignment(1)
    alignment.align(refer_id,image_id)
    print("align done")
    detect = Detect_class(1)
    detect.run(source=image_id)
    print("detect done")

# do image process here
@celery.task(name="targetdetection")
def targetdetection(image_id):
    print("targetdetection work")
    return
