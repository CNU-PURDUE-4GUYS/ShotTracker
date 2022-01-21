from celery import Celery
import os
CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
# celery.conf.timezone = "Asia/Seoul"

@celery.task
def add(x, y):
    print("x is "+x)
    print("y is "+y)
    return x + y
@celery.task(name="hello")
def hello():
    print("hello from celery!!")
    return
