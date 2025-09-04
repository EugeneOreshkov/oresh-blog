from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.sql import func

from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True, nullable=False
    )

    email: so.Mapped[str] = so.mapped_column(
        sa.String(256), index=True, unique=True, nullable=False
    )

    phone: so.Mapped[str] = so.mapped_column(
        sa.String(20), index=True, unique=True, nullable=False
    )

    password_hash: so.Mapped[str] = so.mapped_column(
        sa.String(256), nullable=False
    )

    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    about: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(500), nullable=True
    )

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=func.now(datetime.utcnow()),
        nullable=False,
    )

    last_login: so.Mapped[Optional[datetime]] = so.mapped_column(
        sa.DateTime(timezone=True),
        nullable=True,
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int = 128) -> str:
        """Return the avatar URL (for use in <img src=...>)"""
        import hashlib
        seed = hashlib.md5(self.email.strip().lower().encode("utf-8")).hexdigest()
        return url_for("avatars.avatar", seed=seed, size=size)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Post(db.Model):
    __tablename__ = "posts"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    title: so.Mapped[str] = so.mapped_column(
        sa.String(150), nullable=False
    )
    body: so.Mapped[str] = so.mapped_column(
        sa.Text, nullable=False
    )
    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=func.now(),
        index=True,
        nullable=False,
    )
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("users.id"),
        index=True,
        nullable=False,
    )
    author: so.Mapped["User"] = so.relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post {self.title}>"