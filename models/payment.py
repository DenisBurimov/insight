from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .utils import ModelMixin
from database import db


class Payment(db.Model, ModelMixin):  # type: ignore
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(sa.String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    number: Mapped[str | None] = mapped_column(sa.String(64))
    payment_date: Mapped[str | None] = mapped_column(sa.String(64))
    receiving_date: Mapped[str | None] = mapped_column(sa.String(64))
    summ: Mapped[str | None] = mapped_column(sa.String(64))
    summ_words: Mapped[str | None] = mapped_column(sa.String(512))
    payment_purpose: Mapped[str | None] = mapped_column(sa.String(1024))

    payer_name: Mapped[str | None] = mapped_column(sa.String(128))
    payer_code: Mapped[str | None] = mapped_column(sa.String(10))
    payer_bank_name: Mapped[str | None] = mapped_column(sa.String(512))
    payer_bank_code: Mapped[str | None] = mapped_column(sa.String(512))
    payer_iban: Mapped[str | None] = mapped_column(sa.String(512))

    recipient_name: Mapped[str | None] = mapped_column(sa.String(128))
    recipient_code: Mapped[str | None] = mapped_column(sa.String(10))
    recipient_bank_name: Mapped[str | None] = mapped_column(sa.String(512))
    recipient_bank_code: Mapped[str | None] = mapped_column(sa.String(512))
    recipient_iban: Mapped[str | None] = mapped_column(sa.String(512))

    text_data: Mapped[str | None] = mapped_column(sa.Text)

    def __repr__(self):
        return f"<{self.id}:{self.filename}:{self.summ}>"
