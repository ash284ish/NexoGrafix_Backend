from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.newsletter_subscribers import NewsletterSubscriber
from app.schemas.newsletter_subscriber import (
    NewsletterSubscriberCreate,
    NewsletterSubscriberUpdate,
    NewsletterSubscriberOut,
)

router = APIRouter(prefix="/newsletter-subscribers", tags=["Newsletter Subscribers"])


@router.get("", response_model=list[NewsletterSubscriberOut])
def list_subscribers(db: Session = Depends(get_db), q: str | None = None, limit: int = 50, offset: int = 0):
    stmt = select(NewsletterSubscriber).order_by(NewsletterSubscriber.id.desc()).limit(limit).offset(offset)

    if q:
        like = f"%{q.strip().lower()}%"
        stmt = (
            select(NewsletterSubscriber)
            .where(
                func.lower(NewsletterSubscriber.first_name).like(like)
                | func.lower(NewsletterSubscriber.last_name).like(like)
                | func.lower(NewsletterSubscriber.email).like(like)
            )
            .order_by(NewsletterSubscriber.id.desc())
            .limit(limit)
            .offset(offset)
        )

    return db.execute(stmt).scalars().all()


@router.get("/{subscriber_id}", response_model=NewsletterSubscriberOut)
def get_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    row = db.get(NewsletterSubscriber, subscriber_id)
    if not row:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return row


@router.post("", response_model=NewsletterSubscriberOut, status_code=status.HTTP_201_CREATED)
def create_subscriber(payload: NewsletterSubscriberCreate, db: Session = Depends(get_db)):
    exists = db.execute(
        select(NewsletterSubscriber).where(NewsletterSubscriber.email == str(payload.email).strip().lower())
    ).scalar_one_or_none()

    if exists:
        raise HTTPException(status_code=409, detail="Email already subscribed")

    row = NewsletterSubscriber(
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=str(payload.email).strip().lower(),
        status=payload.status,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/{subscriber_id}", response_model=NewsletterSubscriberOut)
def replace_subscriber(subscriber_id: int, payload: NewsletterSubscriberCreate, db: Session = Depends(get_db)):
    row = db.get(NewsletterSubscriber, subscriber_id)
    if not row:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    email = str(payload.email).strip().lower()
    exists = db.execute(
        select(NewsletterSubscriber).where(NewsletterSubscriber.email == email, NewsletterSubscriber.id != subscriber_id)
    ).scalar_one_or_none()

    if exists:
        raise HTTPException(status_code=409, detail="Email already subscribed")

    row.first_name = payload.first_name.strip()
    row.last_name = payload.last_name.strip()
    row.email = email
    row.status = payload.status

    db.commit()
    db.refresh(row)
    return row


@router.patch("/{subscriber_id}", response_model=NewsletterSubscriberOut)
def update_subscriber(subscriber_id: int, payload: NewsletterSubscriberUpdate, db: Session = Depends(get_db)):
    row = db.get(NewsletterSubscriber, subscriber_id)
    if not row:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    if payload.first_name is not None:
        row.first_name = payload.first_name.strip()

    if payload.last_name is not None:
        row.last_name = payload.last_name.strip()

    if payload.email is not None:
        email = str(payload.email).strip().lower()
        exists = db.execute(
            select(NewsletterSubscriber).where(
                NewsletterSubscriber.email == email, NewsletterSubscriber.id != subscriber_id
            )
        ).scalar_one_or_none()
        if exists:
            raise HTTPException(status_code=409, detail="Email already subscribed")
        row.email = email

    if payload.status is not None:
        row.status = payload.status

    db.commit()
    db.refresh(row)
    return row


@router.delete("/{subscriber_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    row = db.get(NewsletterSubscriber, subscriber_id)
    if not row:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    db.delete(row)
    db.commit()
    return
