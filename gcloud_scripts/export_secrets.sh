#!/bin/bash

echo -n $DIIA_ACCESS_TOKEN | gcloud secrets create DIIA_ACCESS_TOKEN --data-file=-

gcloud secrets add-iam-policy-binding DIIA_ACCESS_TOKEN \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/secretmanager.secretAccessor"

# Add a version from a env variable
echo -n "$DIIA_ACCESS_TOKEN" | gcloud secrets versions add DIIA_ACCESS_TOKEN --data-file=-

# Add a version from a file source
# gcloud secrets versions add OPENAI_API_KEY --data-file="app/services/data/token.pickle"

# echo -n $GMAIL_PICKLE | gcloud secrets create GMAIL_PICKLE --data-file="app/services/data/token.pickle"
