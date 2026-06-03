from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base


class NavMenu(Base):
    __tablename__ = "nav_menus"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )  # main_header, footer, etc.

    title: Mapped[str | None] = mapped_column(String(255))

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
