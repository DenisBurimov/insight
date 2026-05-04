#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# Required env vars (set in .env or export before running):
#
#   PROJECT_ID          GCP project ID
#   REGION              Artifact Registry region  (e.g. europe-west3)
#   ARTIFACT_REPO       Artifact Registry repo name
#   IMAGE_NAME          Docker image name
#   GCE_INSTANCE        GCE instance name
#   GCE_ZONE            GCE instance zone  (e.g. europe-west3-c)
#
# Optional:
#   TAG                 Image tag (defaults to current git short SHA)
# ---------------------------------------------------------------------------

: "${PROJECT_ID:?PROJECT_ID is required}"
: "${REGION:?REGION is required}"
: "${ARTIFACT_REPO:?ARTIFACT_REPO is required}"
: "${IMAGE_NAME:?IMAGE_NAME is required}"
: "${GCE_INSTANCE:?GCE_INSTANCE is required}"
: "${GCE_ZONE:?GCE_ZONE is required}"

TAG="${TAG:-$(git rev-parse --short HEAD)}"

IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REPO}/${IMAGE_NAME}:${TAG}"
LATEST_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${ARTIFACT_REPO}/${IMAGE_NAME}:latest"

echo "==> Building and pushing image: ${IMAGE_URI}"
gcloud builds submit \
  --project="${PROJECT_ID}" \
  --tag="${IMAGE_URI}" \
  .

echo "==> Tagging as latest: ${LATEST_URI}"
gcloud artifacts docker tags add \
  --project="${PROJECT_ID}" \
  "${IMAGE_URI}" \
  "${LATEST_URI}"

echo "==> Deploying to GCE instance: ${GCE_INSTANCE} (${GCE_ZONE})"
gcloud compute ssh "${GCE_INSTANCE}" \
  --zone="${GCE_ZONE}" \
  --project="${PROJECT_ID}" \
  --command="
    set -e
    echo '-- Configuring docker auth for Artifact Registry'
    gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

    echo '-- Pulling new image'
    docker pull ${IMAGE_URI}

    echo '-- Tagging as latest locally'
    docker tag ${IMAGE_URI} ${LATEST_URI}

    echo '-- Restarting container'
    cd /home/app
    IMAGE=${IMAGE_URI} docker compose pull app
    IMAGE=${IMAGE_URI} docker compose up -d --no-build app

    echo '-- Done. Running containers:'
    docker compose ps
  "

echo ""
echo "Deployed ${IMAGE_URI} to ${GCE_INSTANCE}."
