FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD requirements.txt /usr/src/app/
RUN pip install -r requirements.txt
ADD entrypoint.sh /usr/src/app/
ADD . /usr/src/app/ls

CMD python3 backend/manage.py runserver 0.0.0.0:8000  --insecure