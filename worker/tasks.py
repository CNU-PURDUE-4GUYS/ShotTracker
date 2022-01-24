from celery import Celery
import os
CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)
celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
# celery.conf.timezone = "Asia/Seoul"


@celery.task(name="hello")
def hello():
    print("hello from celery!!")
    return



# do yolo work here
@celery.task(name="yolowork")
def yolowork(img_id):
    print(img_id)
    return

# do image process here
@celery.task(name="imageprocessing")
def imageprocessing():
    print("image process work")
    return
