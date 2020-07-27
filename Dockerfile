FROM python:3.8-alpine

RUN adduser -D shorturl

WORKDIR /home/shorturl

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations
COPY shorturl.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP shorturl.py

RUN chown -R shorturl:shorturl ./
USER shorturl

EXPOSE 5000
ENTRYPOINT['./boot.sh']