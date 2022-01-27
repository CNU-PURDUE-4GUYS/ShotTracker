FROM python:3.7

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


RUN python -m pip install --upgrade pip
RUN pip install celery[redis]
# prevent cv2 import error (numpy error)
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY . /queue
WORKDIR /queue

