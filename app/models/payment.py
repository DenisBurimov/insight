from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .utils import ModelMixin
from app import db


class Payment(db.Model, ModelMixin):  # type: ignore
    __tablename__ = "payments"

    # File information
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

    # Document information
    number: Mapped[str | None] = mapped_column(sa.String(64))
    payment_date: Mapped[str | None] = mapped_column(sa.String(8))
    receiving_date: Mapped[str | None] = mapped_column(sa.String(8))
    summ: Mapped[str | None] = mapped_column(sa.Integer)
    summ_words: Mapped[str | None] = mapped_column(sa.String(512))
    payment_purpose: Mapped[str | None] = mapped_column(sa.String(1024))

    # Payer's information
    payer_name: Mapped[str | None] = mapped_column(sa.String(128))
    payer_code: Mapped[str | None] = mapped_column(sa.String(10))
    payer_bank_name: Mapped[str | None] = mapped_column(sa.String(512))
    payer_bank_code: Mapped[str | None] = mapped_column(sa.String(512))
    payer_iban: Mapped[str | None] = mapped_column(sa.String(512))

    # Recipient's information
    recipient_name: Mapped[str | None] = mapped_column(sa.String(128))
    recipient_code: Mapped[str | None] = mapped_column(sa.String(10))
    recipient_bank_name: Mapped[str | None] = mapped_column(sa.String(512))
    recipient_bank_code: Mapped[str | None] = mapped_column(sa.String(512))
    recipient_iban: Mapped[str | None] = mapped_column(sa.String(512))

    def __repr__(self):
        return f"<{self.id}:{self.filename}:{self.summ}>"
