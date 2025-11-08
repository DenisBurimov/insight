import enum
from datetime import datetime, timezone
import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from .utils import ModelMixin
from app import db


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    VIEWER = "viewer"


class User(db.Model, UserMixin, ModelMixin):  # type: ignore
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(128), nullable=True)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True)
    role: Mapped[str] = mapped_column(sa.String(32), default=UserRole.VIEWER.value)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    is_2fa_enabled: Mapped[bool] = mapped_column(sa.Boolean, nullable=True)
    is_notifications_enabled: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=False)

    otp_secret: Mapped[str] = mapped_column(sa.String(64), nullable=True)
    reset_password_token: Mapped[str] = mapped_column(sa.String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter  # type: ignore[no-redef]
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, username, password):
        query = sa.select(cls).where(
            sa.or_(
                sa.func.lower(cls.name) == sa.func.lower(username),
                sa.func.lower(cls.email) == sa.func.lower(username),
            )
        )
        user = db.session.scalar(query)
        if not user:
            return

        if check_password_hash(user.password, password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.name}>"


class AnonymousUser(AnonymousUserMixin):
    pass
