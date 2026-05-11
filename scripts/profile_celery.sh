#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yaml}"
DURATION="${1:-30}"
OUTPUT="flamegraph_celery.svg"

echo "Profiling Celery worker for ${DURATION}s..."

# Oldest celery PID = the main worker process that manages pool subprocesses
PID=$(docker compose -f "$COMPOSE_FILE" exec celery-worker pgrep -o -f 'celery.*worker')

docker compose -f "$COMPOSE_FILE" exec celery-worker \
    py-spy record \
    --output "/tmp/${OUTPUT}" \
    --pid "$PID" \
    --duration "$DURATION" \
    --subprocesses

CONTAINER_ID=$(docker compose -f "$COMPOSE_FILE" ps -q celery-worker)
docker cp "${CONTAINER_ID}:/tmp/${OUTPUT}" "./${OUTPUT}"

echo "Flamegraph saved: ./${OUTPUT}"
open "./${OUTPUT}" 2>/dev/null || true
