from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def seed_admin_user():
    session: Session = SessionLocal()

    email = "ashish@nexographix.com"

    exists = session.query(User.id).filter(User.email == email).first()
    if exists:
        print("Admin user already exists, skipping")
        session.close()
        return

    admin_user = User(
        role_id=1,
        first_name="Ashish",
        last_name="Nexografix",
        email=email,
        phone="+91 96612 84439",
        password_hash=get_password_hash("Nexografix"),
        is_active=True,
    )

    session.add(admin_user)
    session.commit()
    session.close()

    print("Admin user seeded successfully")
