from sqlalchemy import (
    String,
    DateTime,
    Boolean,
    Integer,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base


class PageSection(Base):
    __tablename__ = "page_sections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    page_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("pages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    section_key: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )  # e.g. hero, why_choose_us, testimonials

    section_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # e.g. HERO, CARD_GRID, SLIDER

    title: Mapped[str | None] = mapped_column(String(255))
    subtitle: Mapped[str | None] = mapped_column(String(255))

    order_index: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    data_json: Mapped[str | None] = mapped_column(
        Text
    )  # section-specific JSON payload

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
