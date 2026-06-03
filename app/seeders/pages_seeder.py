from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.page import Page


def seed_pages():
    session: Session = SessionLocal()

    pages = [
        {
            "slug": "home",
            "title": "Home",
            "content": "",
            "meta_title": "Nexografix | AI-enabled Publishing & Content Solutions",
            "meta_description": "AI-enabled services for publishing, content, assessments, and automation.",
            "status": "published",
        },
        {
            "slug": "about-us",
            "title": "About Us",
            "content": "",
            "meta_title": "About Nexografix",
            "meta_description": "Learn more about Nexografix and our AI-enabled publishing services.",
            "status": "published",
        },
        {
            "slug": "contact-us",
            "title": "Contact Us",
            "content": "",
            "meta_title": "Contact Nexografix",
            "meta_description": "Get in touch with Nexografix for publishing and automation services.",
            "status": "published",
        },
        {
            "slug": "faqs",
            "title": "FAQs",
            "content": "",
            "meta_title": "FAQs | Nexografix",
            "meta_description": "Frequently asked questions about Nexografix services and workflows.",
            "status": "published",
        },
        {
            "slug": "feedback",
            "title": "Feedback",
            "content": "",
            "meta_title": "Feedback | Nexografix",
            "meta_description": "Share your feedback with Nexografix.",
            "status": "published",
        },
        {
            "slug": "blogs",
            "title": "Blogs",
            "content": "",
            "meta_title": "Blog | Nexografix",
            "meta_description": "Insights on AI-enabled publishing, automation, and content workflows.",
            "status": "published",
        },
    ]

    for page in pages:
        exists = (
            session.query(Page.id)
            .filter(Page.slug == page["slug"])
            .first()
        )
        if exists:
            continue

        session.add(Page(**page))

    session.commit()
    session.close()

    print("Pages seeded successfully (existing skipped)")
