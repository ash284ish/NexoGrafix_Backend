from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.role import Role


def seed_roles():
    session: Session = SessionLocal()

    roles = [
        {"name": "admin", "description": "Full system access"},
        {"name": "editor", "description": "Can edit pages and blogs"},
        {"name": "author", "description": "Can create blog posts"},
        {"name": "viewer", "description": "Read-only access"},
    ]

    for role_data in roles:
        if session.query(Role.id).filter(Role.name == role_data["name"]).first():
            continue

        session.add(Role(**role_data))

    session.commit()
    session.close()

    print("Roles seeded successfully (existing roles skipped)")
