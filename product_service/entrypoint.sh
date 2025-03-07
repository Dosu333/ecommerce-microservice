#!/bin/sh

python manage.py makemigrations --no-input
python manage.py migrate --no-input
python grpc_server.py &

exec "$@"
