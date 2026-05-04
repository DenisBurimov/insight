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
