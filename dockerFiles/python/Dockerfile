FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk update

RUN apk add --virtual build-deps gcc python-dev musl-dev
RUN apk add postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "tail", "-f", "/dev/null" ]