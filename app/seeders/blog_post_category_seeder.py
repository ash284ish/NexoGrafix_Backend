from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.blog_post import BlogPost
from app.models.blog_category import BlogCategory
from app.models.blog_post_category import BlogPostCategory


def seed_blog_post_categories():
    session: Session = SessionLocal()

    mappings = {
        "delivery-playbook-quality-gates-automation-18": [
            "Publishing & Digitization",
            "Content, eLearning & EdTech",
        ],
        "building-scalable-qa-workflows-publishing": [
            "Publishing & Digitization",
        ],
        "why-automation-critical-modern-content-delivery": [
            "IT & Digital Platforms",
            "Content, eLearning & EdTech",
        ],
        "manuscript-to-market-digitization-best-practices": [
            "Publishing & Digitization",
        ],
        "improving-delivery-slas-structured-checkpoints": [
            "Publishing & Digitization",
        ],
        "xml-first-publishing-when-and-why": [
            "Publishing & Digitization",
        ],
        "accessibility-compliance-digital-publishing": [
            "Accessibility & Compliance",
        ],
        "reducing-rework-better-content-planning": [
            "Content, eLearning & EdTech",
        ],
        "automating-quality-checks-large-scale-publishing": [
            "Publishing & Digitization",
            "IT & Digital Platforms",
        ],
        "lessons-learned-high-volume-content-delivery": [
            "Content, eLearning & EdTech",
        ],
    }

    for post_slug, category_names in mappings.items():
        post = session.query(BlogPost).filter(BlogPost.slug == post_slug).first()
        if not post:
            continue

        for category_name in category_names:
            category = (
                session.query(BlogCategory)
                .filter(BlogCategory.name == category_name)
                .first()
            )
            if not category:
                continue

            exists = (
                session.query(BlogPostCategory.id)
                .filter(
                    BlogPostCategory.post_id == post.id,
                    BlogPostCategory.category_id == category.id,
                )
                .first()
            )
            if exists:
                continue

            session.add(
                BlogPostCategory(
                    post_id=post.id,
                    category_id=category.id,
                )
            )

    session.commit()
    session.close()

    print("Blog post categories seeded successfully (existing skipped)")
