from sqlalchemy import String, Text, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.db.base import Base


def now_utc():
    return datetime.now(timezone.utc)


class Feedback(Base):
    __tablename__ = "feedbacks"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # User identity
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    role: Mapped[str] = mapped_column(String(120), nullable=True)
    company: Mapped[str] = mapped_column(String(150), nullable=True)

    # Feedback content
    service: Mapped[str] = mapped_column(String(120), nullable=False, index=True)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)  
    # 1–5 stars

    rating_label: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True
    )
    # good / average / bad

    message: Mapped[str] = mapped_column(Text, nullable=False)

    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Publish & moderation
    can_publish: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    publish_status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        nullable=False,
        index=True
    )
    # pending / approved / rejected

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
        index=True
    )
    # active / hidden / deleted

    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Admin / meta
    source: Mapped[str] = mapped_column(String(50), default="website_form", nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_utc,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=now_utc,
        onupdate=now_utc,
        nullable=False
    )
