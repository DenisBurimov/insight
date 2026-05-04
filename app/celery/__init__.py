import os
from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "app",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
)

celery.conf.update(
    timezone="UTC",
    enable_utc=True,
    include=["app.celery.mails"],
)

celery.conf.beat_schedule = {
    "fetch-emails-every-hour": {
        "task": "app.celery.mails.fetch_emails",
        "schedule": crontab(minute=0),
    },
}
