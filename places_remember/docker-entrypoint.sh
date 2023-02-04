#!/bin/bash

# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Start server in production or development mode
if [$DEPLOY_MODE == "DEV"]; then
    echo "Starting server in development mode"
    uvicorn places_remember.asgi:application --proxy-headers --forwarded-allow-ips='*' --reload --host 0.0.0.0
else
    echo "Starting server in production mode"
    gunicorn -w $N_UVICORN_WORKERS -k uvicorn.workers.UvicornWorker --proxy-protocol --forwarded-allow-ips='*' --bind 0.0.0.0 places_remember.asgi:application
fi