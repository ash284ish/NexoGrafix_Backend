from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class BlogPostCategory(Base):
    __tablename__ = "blog_post_categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    post_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("blog_posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("blog_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
