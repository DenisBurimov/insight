#!/bin/sh
echo "Waiting for Flask app to be ready..."
until curl -sf http://app:8080/no-content > /dev/null; do
  echo "Flask app not ready, retrying in 3s..."
  sleep 3
done
echo "Flask app is ready, starting API server"
exec uvicorn api.main:app --host 0.0.0.0 --port 8001
