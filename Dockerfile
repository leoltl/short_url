FROM python:3.8-alpine

RUN adduser -D shorturl

WORKDIR /home/shorturl

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY shorturl.py config.py utils.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP shorturl.py

RUN chown -R shorturl:shorturl ./
USER shorturl

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]


# command on docker build/ run
# docker build -t <image-name> . 
# docker run -d --name <container-name> -p <incoming-port>:5000 --mount type=bind,source=/home/pi/certs,target=/certs <image-name>
