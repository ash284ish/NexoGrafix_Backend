from sqlalchemy import (
    String,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base


class NavMenuItem(Base):
    __tablename__ = "nav_menu_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    menu_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("nav_menus.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("nav_menu_items.id", ondelete="CASCADE"),
    )  # dropdown nesting

    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    href: Mapped[str | None] = mapped_column(String(255))  # external/internal URL

    page_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("pages.id", ondelete="SET NULL"),
    )  # optional CMS page link

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
