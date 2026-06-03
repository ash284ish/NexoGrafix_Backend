from sqlalchemy import (
    String,
    DateTime,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base


class PageSectionMedia(Base):
    __tablename__ = "page_section_media"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    page_section_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("page_sections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    media_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("media_assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[str | None] = mapped_column(
        String(50)
    )  # bg, thumbnail, icon, hero_image, card_image

    order_index: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
