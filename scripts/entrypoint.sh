#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

echo "Waiting for Memcached..."
while ! nc -z memcached 11211; do
    sleep 0.1
done
echo "Memcached started"

echo "Running migrations..."
python manage.py migrate --no-input

echo "Starting server..."
exec "$@" 