#!/usr/bin/env python3
import os
import subprocess
import sys
from dotenv import load_dotenv


load_dotenv()


def run_cmd(
    cmd: list[str], check=True, capture_output=False
) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=capture_output)


CLOUD_RUN_SERVICE = os.environ.get("CLOUD_RUN_SERVICE")
CLOUD_RUN_REGION = os.environ.get("CLOUD_RUN_REGION")
SPANNER_PROJECT_ID = os.environ.get("SPANNER_PROJECT_ID")
ARTIFACT_REPO = os.environ.get("ARTIFACT_REPO")
IMG_NAME = os.environ.get("IMG_NAME")
TAG_NAME = os.environ.get("TAG_NAME")

if not all(
    [
        CLOUD_RUN_SERVICE,
        CLOUD_RUN_REGION,
        SPANNER_PROJECT_ID,
        ARTIFACT_REPO,
        IMG_NAME,
        TAG_NAME,
    ]
):
    print("❌ Missing required environment variables.")
    sys.exit(1)

MAKE_EXISTING_PUBLIC_TOO = True

image_path = f"{CLOUD_RUN_REGION}-docker.pkg.dev/{SPANNER_PROJECT_ID}/{ARTIFACT_REPO}/{IMG_NAME}:{TAG_NAME}"

secrets = [
    "APP_ENV=APP_ENV:latest",
    "APP_NAME=APP_NAME:latest",
    "SECRET_KEY=SECRET_KEY:latest",
    "DATABASE_CONNECTION=DATABASE_CONNECTION:latest",
    "SCHEDULER_ACCESS_TOKEN=SCHEDULER_ACCESS_TOKEN:latest",
    "SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI:latest",
    "OPENAI_API_KEY=OPENAI_API_KEY:latest",
    "VECTOR_STORE_ID=VECTOR_STORE_ID:latest",
    "ADMIN_USERNAME=ADMIN_USERNAME:latest",
    "ADMIN_EMAIL=ADMIN_EMAIL:latest",
    "ADMIN_PASSWORD=ADMIN_PASSWORD:latest",
    "INSTANCE_CONNECTION_NAME=INSTANCE_CONNECTION_NAME:latest",
    "POSTGRES_USER=POSTGRES_USER:latest",
    "POSTGRES_PASSWORD=POSTGRES_PASSWORD:latest",
    "POSTGRES_DB=POSTGRES_DB:latest",
]


def service_exists() -> bool:
    try:
        run_cmd(
            [
                "gcloud",
                "run",
                "services",
                "describe",
                CLOUD_RUN_SERVICE,
                "--region",
                CLOUD_RUN_REGION,
                "--platform",
                "managed",
                "--format",
                "value(metadata.name)",
            ],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


is_existing = service_exists()

gcloud_command = [
    "gcloud",
    "run",
    "deploy",
    CLOUD_RUN_SERVICE,
    "--image",
    image_path,
    "--cpu",
    "4",
    "--memory",
    "16Gi",
    "--platform",
    "managed",
    "--region",
    CLOUD_RUN_REGION,
    "--timeout",
    "15m",
    "--set-secrets",
    ",".join(secrets),
    # "--concurrency", "80",
    # "--min-instances", "0",
    # "--max-instances", "10",
    # "--service-account", "your-sa@project.iam.gserviceaccount.com",
    # "--port", "8080",
]

if not is_existing:
    gcloud_command.append("--allow-unauthenticated")

try:
    run_cmd(gcloud_command, check=True)
    print("✅ Deployment successful!")
except subprocess.CalledProcessError as e:
    print("❌ Deployment failed:", e)
    sys.exit(e.returncode)

# If service already existed and you also want it public, add the invoker binding
if is_existing and MAKE_EXISTING_PUBLIC_TOO:
    try:
        run_cmd(
            [
                "gcloud",
                "run",
                "services",
                "add-iam-policy-binding",
                CLOUD_RUN_SERVICE,
                "--region",
                CLOUD_RUN_REGION,
                "--platform",
                "managed",
                "--member",
                "allUsers",
                "--role",
                "roles/run.invoker",
            ],
            check=True,
        )
        print(
            "🔓 Existing service made publicly accessible (roles/run.invoker granted to allUsers)."
        )
    except subprocess.CalledProcessError as e:
        print(
            "⚠️ Failed to add public invoker role (service may already be public or permissions missing):",
            e,
        )
