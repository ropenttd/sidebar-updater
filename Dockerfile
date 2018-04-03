FROM python:2.7-alpine

LABEL maintainer="duck <me@duck.me.uk>"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache -r requirements.txt

COPY . /app

CMD ["python", "/app/update.py"]