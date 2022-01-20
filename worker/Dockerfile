FROM python:3.7

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

COPY . /queue
WORKDIR /queue

RUN python -m pip install --upgrade pip
RUN pip install celery[redis]

# YoloV5 requirements Download
RUN pip install -r requirements.txt

# prevent cv2 import error (numpy error)
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

