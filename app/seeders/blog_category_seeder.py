from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.blog_category import BlogCategory
from slugify import slugify


def seed_blog_categories():
    session: Session = SessionLocal()

    categories = [
        # Core Solutions
        "Publishing & Digitization",
        "Accessibility & Compliance",
        "IT & Digital Platforms",
        "Data Labeling & Annotation",
        "Localization & Media Accessibility",
        "Content, eLearning & EdTech",

        # Publishing & Digitization – Services
        "Document Digitization & Scanning",
        "Copyediting & Proofreading",
        "eBook Conversion (EPUB & Kindle)",
        "XML & HTML Conversion",
        "Typesetting & Layout Design",
        "Metadata Creation & Tagging",
        "Multimedia Integration",
        "Interactive eBook Development",
        "Print-on-Demand (POD) Preparation",
        "Magazine & Newspaper Digitization",

        # Cross-cutting / Tech-focused
        "Digital Publishing Platforms",
        "Content Automation",
        "AI in Publishing",
        "Workflow Optimization",
        "Publishing Compliance & Standards",
    ]

    for name in categories:
        slug = slugify(name)

        exists = (
            session.query(BlogCategory.id)
            .filter(BlogCategory.slug == slug)
            .first()
        )
        if exists:
            continue

        session.add(
            BlogCategory(
                name=name,
                slug=slug,
            )
        )

    session.commit()
    session.close()

    print("Blog categories seeded successfully (existing skipped)")
