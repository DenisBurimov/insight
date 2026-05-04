from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .utils import ModelMixin
from database import db


class Mail(db.Model, ModelMixin):  # type: ignore
    __tablename__ = "mails"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message_id: Mapped[str] = mapped_column(sa.String(128), unique=True, index=True)
    thread_id: Mapped[str | None] = mapped_column(sa.String(128))
    subject: Mapped[str | None] = mapped_column(sa.String(512))
    sender: Mapped[str | None] = mapped_column(sa.String(256))
    recipient: Mapped[str | None] = mapped_column(sa.String(256))
    snippet: Mapped[str | None] = mapped_column(sa.String(1024))
    received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<Mail {self.message_id}: {self.subject}>"
