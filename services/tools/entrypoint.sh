#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "Starting ol api"

python3 manage.py run -h 0.0.0.0
