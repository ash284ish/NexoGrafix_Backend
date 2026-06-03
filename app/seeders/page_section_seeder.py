from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.page_section import PageSection
import json


def seed_blog_page_top_section():
    session: Session = SessionLocal()

    # page_id = 6 (Blogs page)
    section_key = "top"

    exists = (
        session.query(PageSection.id)
        .filter(
            PageSection.page_id == 6,
            PageSection.section_key == section_key
        )
        .first()
    )

    if exists:
        print("Blog top section already exists, skipping")
        session.close()
        return

    section = PageSection(
        page_id=6,
        section_key="top",
        section_type="HEADING",
        title="Insights that improve delivery.",
        subtitle="Actionable reads on AI-enabled publishing, content workflows, automation, and product engineering.",
        order_index=0,
        is_enabled=True,
        data_json=json.dumps({
            "badge": "BLOG",
            "alignment": "center"
        }),
    )

    session.add(section)
    session.commit()
    session.close()

    print("Blog top section seeded successfully")
