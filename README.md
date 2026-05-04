# Flask dashboard for OCR using cloud or local LLMs & Chatbot
# FastAPI endpoints for MCP

![Description](app/static/img/screen_01.png)
![Description](app/static/img/screen_02.png)


## To run the project locally set up venv and activate it
```
python3.13 -m venv .venv
source .venv/bin/activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## Set up environment variables
```
cp .env.example .env
# edit .env with your actual values
```

## Use make command to run a local postgres db
```
make dcupd
```

## Run migrations
```
flask db upgrade
```

## Create an admin user
```
flask create-admin
```

## If you use vscode, run the debug configuration Python: Flask

## If not
```
flask run --port 5050
```

## Run the FastAPI MCP server
```
uvicorn api.main:app --port 8001 --reload
```
The MCP endpoint will be available at `http://localhost:8001/mcp`.

## Run tests
```
pytest
```

## To run the app in docker compose locally or on GCE
```
docker compose build
docker compose up
```

## Use docker-compose.traefik to set up a reverse proxy on a linux server such as GCE etc.

## Deploy to GCE via Artifact Registry

### One-time: push secrets to GCP Secret Manager
Edit `gcloud_scripts/export_secrets.sh` to add each secret you need (one block per secret),
then run it once per secret:
```bash
export SERVICE_ACCOUNT_EMAIL=your-sa@your-project.iam.gserviceaccount.com
export SECRET_NAME=OPENAI_API_KEY
export SECRET_VALUE=sk-...

bash gcloud_scripts/export_secrets.sh
```

### Deploy
Export the required variables, then run the deploy script:
```bash
export PROJECT_ID=your-gcp-project-id
export REGION=europe-west3
export ARTIFACT_REPO=your-artifact-repo-name
export IMAGE_NAME=insight
export GCE_INSTANCE=your-gce-instance-name
export GCE_ZONE=europe-west3-c

bash gcloud/gce_deploy.sh
```
The script builds the Docker image in the cloud (`gcloud builds submit`), pushes it to Artifact Registry tagged with the current git SHA and `:latest`, then SSHes into the GCE instance and restarts the container.

Optionally override the image tag:
```bash
TAG=v1.2.3 bash gcloud/gce_deploy.sh
```

## To connect Claude Web to the MCP go to Settings - Connectors - Add a custom connector
Use the URL of your deployed MCP server: `https://your-domain.com/mcp`

## Deploy to GKE

Kubernetes manifests live in `gke/`. The stack deploys five workloads:

| Manifest | Workload |
|---|---|
| `redis.yaml` | Redis broker + result backend |
| `web.yaml` | Flask / gunicorn (port 8080) |
| `api.yaml` | FastAPI MCP server / uvicorn (port 8001) |
| `celery-worker.yaml` | Celery worker |
| `celery-beat.yaml` | Celery beat scheduler (StatefulSet) |

### One-time setup

**Reserve a static external IP**
```bash
gcloud compute addresses create insight-ip --global
gcloud compute addresses describe insight-ip --global   # copy the IP value
```
Point your domain's A record to that IP.

**Create the Gmail token secret** (if the app uses Gmail OAuth)
```bash
kubectl create secret generic gmail-token -n insight \
  --from-file=token.pickle=./token.pickle
```

**Configure Workload Identity** (so pods can access GCP Secret Manager)
```bash
gcloud iam service-accounts add-iam-policy-binding \
  insight-sa@PROJECT_ID.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT_ID.svc.id.goog[insight/insight-sa]"
```

### Before applying

1. Replace the `image:` placeholder in `web.yaml`, `api.yaml`, `celery-worker.yaml`, `celery-beat.yaml`, and `migrate-job.yaml`:
   ```
   REGION-docker.pkg.dev/PROJECT_ID/ARTIFACT_REPO/insight:latest
   ```
2. Fill in real values in `gke/secret.yaml` (or skip the file and use `kubectl create secret` directly):
   ```bash
   kubectl create secret generic insight-secrets -n insight \
     --from-literal=SECRET_KEY=... \
     --from-literal=SQLALCHEMY_DATABASE_URI=postgresql://user:pass@host:5432/insight \
     --from-literal=OPENAI_API_KEY=sk-... \
     --from-literal=SCHEDULER_ACCESS_TOKEN=... \
     --from-literal=ADMIN_USERNAME=admin \
     --from-literal=ADMIN_EMAIL=admin@example.com \
     --from-literal=ADMIN_PASSWORD=...
   ```
3. Replace `your-domain.com` in `gke/ingress.yaml`.

### Apply

```bash
kubectl apply -f gke/namespace.yaml
kubectl apply -f gke/serviceaccount.yaml
kubectl apply -f gke/configmap.yaml
kubectl apply -f gke/secret.yaml

# Redis must be ready before the app starts
kubectl apply -f gke/redis.yaml
kubectl rollout status deployment/redis -n insight

# Run database migrations
kubectl apply -f gke/migrate-job.yaml
kubectl wait --for=condition=complete job/migrate -n insight --timeout=120s

# Deploy application workloads
kubectl apply -f gke/web.yaml \
              -f gke/api.yaml \
              -f gke/celery-worker.yaml \
              -f gke/celery-beat.yaml

# Ingress and autoscalers
kubectl apply -f gke/ingress.yaml
kubectl apply -f gke/hpa.yaml
```

### Notes

- **Scaling the web pod**: `web.yaml` uses a single replica because the payments PVC is `ReadWriteOnce`. To run multiple replicas, migrate payment file storage to GCS or GKE Filestore and switch `accessModes` to `ReadWriteMany`.
- **Celery beat**: only one replica is supported — multiple instances would fire duplicate tasks.
- **Migrations on redeploy**: delete and re-apply `migrate-job.yaml` before rolling out a new image:
  ```bash
  kubectl delete job migrate -n insight --ignore-not-found
  kubectl apply -f gke/migrate-job.yaml
  kubectl wait --for=condition=complete job/migrate -n insight --timeout=120s
  ```
