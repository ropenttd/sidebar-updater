FROM python:2.7-alpine

LABEL maintainer="duck <me@duck.me.uk>"

RUN apk add --update git
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache -r requirements.txt

COPY . /app

CMD ["sh", "/app/entrypoint.sh"]
