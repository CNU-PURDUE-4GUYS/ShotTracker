FROM python:3.9

EXPOSE 5000

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

ADD requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["flask", "run"]
