from sqlalchemy import String, DateTime, Enum, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    kind: Mapped[str] = mapped_column(
        Enum("image", "video", "icon", "doc", name="media_asset_kind"),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(Text, nullable=False)

    alt_text: Mapped[str | None] = mapped_column(String(255))
    caption: Mapped[str | None] = mapped_column(String(255))

    width: Mapped[int | None] = mapped_column(Integer)
    height: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
