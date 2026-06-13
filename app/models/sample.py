from sqlalchemy import String, DateTime, Text, JSON, Integer, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import List, Any
from app.db.base import Base
from app.models.sample_category import SampleCategory
from app.models.sample_industry import SampleIndustry

# Many-to-many associations
sample_category_association = Table(
    "sample_category_association",
    Base.metadata,
    Column("sample_id", Integer, ForeignKey("samples.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("sample_categories.id", ondelete="CASCADE"), primary_key=True),
)

sample_industry_association = Table(
    "sample_industry_association",
    Base.metadata,
    Column("sample_id", Integer, ForeignKey("samples.id", ondelete="CASCADE"), primary_key=True),
    Column("industry_id", Integer, ForeignKey("sample_industries.id", ondelete="CASCADE"), primary_key=True),
)

class Sample(Base):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    short_description: Mapped[str] = mapped_column(String(500), nullable=False)
    detailed_description: Mapped[str] = mapped_column(Text, nullable=False)
    featured_image: Mapped[str | None] = mapped_column(String(500))
    video_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="published", nullable=False)  # draft, published
    visibility: Mapped[str] = mapped_column(String(30), default="public", nullable=False)  # public, private, password_protected
    password: Mapped[str | None] = mapped_column(String(255))
    
    # JSON columns for list types
    technologies: Mapped[Any | None] = mapped_column(JSON)       # List of strings
    project_highlights: Mapped[Any | None] = mapped_column(JSON) # List of strings
    client_outcome: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[Any | None] = mapped_column(JSON)               # List of strings
    gallery_images: Mapped[Any | None] = mapped_column(JSON)     # List of strings/URLs
    before_after_images: Mapped[Any | None] = mapped_column(JSON) # E.g. {"before": "...", "after": "..."}
    screenshots: Mapped[Any | None] = mapped_column(JSON)        # List of strings/URLs
    download_files: Mapped[Any | None] = mapped_column(JSON)     # List of dicts: [{"name": "file.pdf", "url": "..."}]

    # SEO fields
    seo_title: Mapped[str | None] = mapped_column(String(255))
    seo_meta_description: Mapped[str | None] = mapped_column(String(500))
    seo_meta_keywords: Mapped[str | None] = mapped_column(String(500))
    seo_og_image: Mapped[str | None] = mapped_column(String(500))
    seo_canonical_url: Mapped[str | None] = mapped_column(String(500))

    # Analytics
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    downloads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    categories: Mapped[List[SampleCategory]] = relationship(
        secondary=sample_category_association,
        backref="samples"
    )
    industries: Mapped[List[SampleIndustry]] = relationship(
        secondary=sample_industry_association,
        backref="samples"
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
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
