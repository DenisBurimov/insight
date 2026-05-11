# Observability TODO

## Phase 1 — Prometheus (Metrics)

### App instrumentation
- [ ] Add `prometheus-flask-exporter` to `requirements.txt`
- [ ] Add `prometheus-fastapi-instrumentator` to `requirements.txt`
- [ ] Init `PrometheusMetrics(app)` in `app/__init__.py` → exposes `/metrics` on Flask
- [ ] Init `Instrumentator().instrument(app).expose(app)` in `api/main.py` → exposes `/metrics` on FastAPI
- [ ] Add custom Celery metrics using `prometheus_client` (task count, duration, failure rate per task name)
  - Create `app/metrics.py` with `Counter`/`Histogram` for Celery signals (`task_prerun`, `task_postrun`, `task_failure`)

### Exporters
- [ ] Add `prom/redis-exporter` service to `docker-compose.yaml` (scrapes Redis on port 9121)
- [ ] Add `prometheuscommunity/postgres-exporter` service to `docker-compose.yaml` (scrapes Postgres on port 9187)

### Prometheus server
- [ ] Create `monitoring/prometheus/prometheus.yml` with scrape configs:
  - Flask app (`app:8080/metrics`)
  - FastAPI (`api:8001/metrics`)
  - Redis exporter (`:9121/metrics`)
  - Postgres exporter (`:9187/metrics`)
- [ ] Add `prometheus` service to `docker-compose.yaml` (port 9090), mounting `prometheus.yml`

### GKE
- [ ] Add `gke/prometheus.yaml` — Deployment + Service for Prometheus
- [ ] Add `gke/redis-exporter.yaml` — Deployment + Service
- [ ] Add `gke/postgres-exporter.yaml` — Deployment + Service
- [ ] Add `prometheus.io/scrape: "true"` annotations to existing pod specs in `gke/web.yaml`, `gke/api.yaml`, `gke/celery-worker.yaml`

---

## Phase 2 — Loki (Log Aggregation)

### Structured logging
- [ ] Update `app/logger.py` to emit JSON-structured logs (add `python-json-logger` to `requirements.txt`)
  - Fields: `timestamp`, `level`, `message`, `service`, `trace_id` (optional)
- [ ] Set `LOG_FORMAT=json` toggle via env var so dev stays human-readable

### Loki + Promtail (Docker Compose)
- [ ] Create `monitoring/loki/loki-config.yaml` (filesystem storage, single-binary mode)
- [ ] Create `monitoring/promtail/promtail-config.yaml`
  - Scrape Docker container logs from `/var/lib/docker/containers/*/*-json.log`
  - Label by `container_name`, `service`
- [ ] Add `loki` service to `docker-compose.yaml` (port 3100), mounting `loki-config.yaml`
- [ ] Add `promtail` service to `docker-compose.yaml`, mounting Docker socket + `promtail-config.yaml`

### GKE
- [ ] Add `gke/loki.yaml` — StatefulSet + Service (or use Grafana Cloud Loki endpoint)
- [ ] Add `gke/promtail.yaml` — DaemonSet that reads pod logs from `/var/log/pods` and ships to Loki

---

## Phase 3 — Grafana (Dashboards)

### Setup
- [ ] Add `grafana/oss` service to `docker-compose.yaml` (port 3000)
- [ ] Create `monitoring/grafana/provisioning/datasources/datasources.yaml`
  - Prometheus datasource → `http://prometheus:9090`
  - Loki datasource → `http://loki:3100`
- [ ] Create `monitoring/grafana/provisioning/dashboards/dashboards.yaml` (dashboard provider config)

### Dashboards (JSON files in `monitoring/grafana/dashboards/`)
- [ ] `flask-overview.json` — request rate, p50/p95/p99 latency, error rate, active connections
- [ ] `fastapi-overview.json` — same RED metrics for FastAPI
- [ ] `celery-tasks.json` — task throughput, queue depth, failure rate per task name, avg duration
- [ ] `redis.json` — memory usage, hit/miss ratio, connected clients, ops/sec
- [ ] `postgres.json` — active connections, query duration, transaction rate, pgbouncer pool stats

### GKE
- [ ] Add `gke/grafana.yaml` — Deployment + Service + PersistentVolumeClaim

---

## Phase 4 — py-spy (Profiling)

### Scripts
- [ ] Create `scripts/profile_web.sh`
  - Finds the Gunicorn master PID inside the running `app` container
  - Runs `py-spy record -o flamegraph_web.svg --pid <PID> --duration 30`
- [ ] Create `scripts/profile_api.sh`
  - Same but targets the Uvicorn process in the `api` container
- [ ] Create `scripts/profile_celery.sh`
  - Profiles a running Celery worker for 30s
- [ ] Add `py-spy` to `requirements.txt` (or keep as dev-only in `pyproject.toml`)

### Makefile targets
- [ ] `make profile-web` — runs `scripts/profile_web.sh`, opens `flamegraph_web.svg`
- [ ] `make profile-api` — runs `scripts/profile_api.sh`, opens `flamegraph_api.svg`
- [ ] `make profile-celery` — runs `scripts/profile_celery.sh`

### Docker requirements for py-spy
- [ ] Add `--cap-add SYS_PTRACE` to `app` and `api` services in `docker-compose.yaml` (needed for py-spy to attach)
- [ ] Document GKE ephemeral container approach in `README.md`:
  ```
  kubectl debug -it <pod> --image=jonringer/py-spy --target=<container> -- py-spy record -o /tmp/flamegraph.svg --pid 1 --duration 30
  ```

---

## Suggested directory layout

```
monitoring/
  prometheus/
    prometheus.yml
  loki/
    loki-config.yaml
  promtail/
    promtail-config.yaml
  grafana/
    provisioning/
      datasources/
        datasources.yaml
      dashboards/
        dashboards.yaml
    dashboards/
      flask-overview.json
      fastapi-overview.json
      celery-tasks.json
      redis.json
      postgres.json
scripts/
  profile_web.sh
  profile_api.sh
  profile_celery.sh
```
