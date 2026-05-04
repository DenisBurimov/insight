import enum
from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .utils import ModelMixin, gen_uuid
from database import db


class MessageSender(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(db.Model, ModelMixin):  # type: ignore
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[str] = mapped_column(sa.String(36), unique=True, default=lambda: gen_uuid())
    room_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    role: Mapped[MessageSender] = mapped_column(sa.String(16), nullable=False, default=MessageSender.USER.value)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<{self.id}: {self.role} - {self.content[:20]}...>"
