from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.page import PageName


def seed_pages_name():
    session: Session = SessionLocal()

    pages = [
        {
            "slug": "home",
            "title": "Home",
            "meta_title": "Nexografix | AI-enabled Publishing & Content Solutions",
            "meta_description": "AI-enabled services for publishing, content, assessments, and automation.",
        },
        {
            "slug": "about-us",
            "title": "About Us",
            "meta_title": "About Nexografix",
            "meta_description": "Learn more about Nexografix and our AI-enabled publishing services.",
        },
        {
            "slug": "contact-us",
            "title": "Contact Us",
            "meta_title": "Contact Nexografix",
            "meta_description": "Get in touch with Nexografix for publishing and automation services.",
        },
        {
            "slug": "faqs",
            "title": "FAQs",
            "meta_title": "FAQs | Nexografix",
            "meta_description": "Frequently asked questions about Nexografix services and workflows.",
        },
        {
            "slug": "feedback",
            "title": "Feedback",
            "meta_title": "Feedback | Nexografix",
            "meta_description": "Share your feedback with Nexografix.",
        },
        {
            "slug": "blogs",
            "title": "Blogs",
            "meta_title": "Blog | Nexografix",
            "meta_description": "Insights on AI-enabled publishing, automation, and content workflows.",
        },
    ]

    for page in pages:
        exists = (
            session.query(PageName.id)
            .filter(PageName.slug == page["slug"])
            .first()
        )
        if exists:
            continue

        session.add(
            PageName(
                slug=page["slug"],
                title=page["title"],
                meta_title=page["meta_title"],
                meta_description=page["meta_description"],
                is_published=True,
            )
        )

    session.commit()
    session.close()

    print("Pages seeded successfully (existing skipped)")
