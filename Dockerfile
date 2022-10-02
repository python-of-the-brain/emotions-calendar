FROM  python:3.10-slim


ENV TZ="Europe/Moscow"
RUN pip install -U pip  --no-cache-dir

ADD ./back/requirements.txt /requirements.txt

RUN pip install -r requirements.txt

WORKDIR /back
COPY ./back /back
