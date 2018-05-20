FROM python:3.6.4-slim-jessie
RUN apt-get update && apt-get install libgomp1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
ADD . /usr/src/app
CMD python3 -u streamer/streamer.py
