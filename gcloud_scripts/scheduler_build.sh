gcloud scheduler jobs create http $SCHEDULER_NAME --schedule "* */13 * * *" --uri $SCHEDULER_TARGET --http-method GET --oidc-service-account-email $SERVICE_ACCOUNT_EMAIL --location europe-west3
