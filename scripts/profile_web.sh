#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yaml}"
DURATION="${1:-30}"
OUTPUT="flamegraph_web.svg"

echo "Profiling Flask/Gunicorn for ${DURATION}s..."

# Oldest gunicorn PID = master process; --subprocesses captures all workers
PID=$(docker compose -f "$COMPOSE_FILE" exec app pgrep -o -f gunicorn)

docker compose -f "$COMPOSE_FILE" exec app \
    py-spy record \
    --output "/tmp/${OUTPUT}" \
    --pid "$PID" \
    --duration "$DURATION" \
    --subprocesses

CONTAINER_ID=$(docker compose -f "$COMPOSE_FILE" ps -q app)
docker cp "${CONTAINER_ID}:/tmp/${OUTPUT}" "./${OUTPUT}"

echo "Flamegraph saved: ./${OUTPUT}"
open "./${OUTPUT}" 2>/dev/null || true
