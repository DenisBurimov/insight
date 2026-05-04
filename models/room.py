from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .utils import ModelMixin, gen_uuid
from database import db


class Room(db.Model, ModelMixin):  # type: ignore
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(sa.String(36), unique=True, default=lambda: gen_uuid())
    user_id: Mapped[int] = mapped_column(sa.Integer, ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship("User", back_populates="rooms")

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
