FROM python:3.9

EXPOSE 8001


ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true


ENV HOST 0.0.0.0
ENV PORT 5000
ENV DEBUG true


ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

WORKDIR /app
COPY . /app
RUN pip install Pillow

ADD requirements.txt .
RUN pip install -r requirements.txt



CMD ["python","-u","app.py"]
