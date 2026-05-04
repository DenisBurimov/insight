import pickle
from datetime import datetime, timezone

import sqlalchemy as sa
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from app.celery import celery
from app.logger import log


@celery.task
def fetch_emails():
    from app import create_app
    from database import db
    import models as m
    from config import config

    CFG = config()
    app = create_app()

    with app.app_context():
        try:
            with open(CFG.GMAIL_TOKEN_PATH, "rb") as fh:
                creds = pickle.load(fh)

            if creds.expired and creds.refresh_token:
                creds.refresh(Request())

            service = build("gmail", "v1", credentials=creds)
            results = service.users().messages().list(userId="me").execute()
            messages = results.get("messages", [])

            saved = 0
            for msg_ref in messages:
                msg_id = msg_ref["id"]

                if db.session.scalar(sa.select(m.Mail).where(m.Mail.message_id == msg_id)):
                    continue

                msg = service.users().messages().get(
                    userId="me", id=msg_id, format="full"
                ).execute()
                headers = {
                    h["name"]: h["value"]
                    for h in msg.get("payload", {}).get("headers", [])
                }

                m.Mail(
                    message_id=msg_id,
                    thread_id=msg.get("threadId"),
                    subject=headers.get("Subject", "")[:512],
                    sender=headers.get("From", "")[:256],
                    recipient=headers.get("To", "")[:256],
                    snippet=msg.get("snippet", "")[:1024],
                    received_at=datetime.fromtimestamp(
                        int(msg["internalDate"]) / 1000, tz=timezone.utc
                    ),
                ).save()
                saved += 1

            log(log.INFO, "fetch_emails: saved %d new messages", saved)

        except Exception as e:
            log(log.ERROR, "fetch_emails failed: %s", e)
            raise
