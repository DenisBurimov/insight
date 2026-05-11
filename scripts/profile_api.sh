#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yaml}"
DURATION="${1:-30}"
OUTPUT="flamegraph_api.svg"

echo "Profiling FastAPI/Gunicorn+Uvicorn for ${DURATION}s..."

# start_api.sh uses exec, so gunicorn is PID 1; --subprocesses captures uvicorn workers
PID=$(docker compose -f "$COMPOSE_FILE" exec api pgrep -o -f gunicorn)

docker compose -f "$COMPOSE_FILE" exec api \
    py-spy record \
    --output "/tmp/${OUTPUT}" \
    --pid "$PID" \
    --duration "$DURATION" \
    --subprocesses

CONTAINER_ID=$(docker compose -f "$COMPOSE_FILE" ps -q api)
docker cp "${CONTAINER_ID}:/tmp/${OUTPUT}" "./${OUTPUT}"

echo "Flamegraph saved: ./${OUTPUT}"
open "./${OUTPUT}" 2>/dev/null || true
