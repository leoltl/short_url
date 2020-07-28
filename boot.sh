#!/bin/sh
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - --certfile /certs/fullchain.pem --keyfile /certs/privkey.pem shorturl:app