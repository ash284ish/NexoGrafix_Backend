from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.contact_requests import ContactRequest
from app.models.newsletter_subscribers import NewsletterSubscriber  # make sure this exists
from app.schemas.stats import StatsOut

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("", response_model=StatsOut)
def get_stats(db: Session = Depends(get_db)):
    # Newsletter subscribers count
    total_newsletters = db.execute(
        select(func.count()).select_from(NewsletterSubscriber)
    ).scalar_one()

    # Contact request status-wise counts
    total_new = db.execute(
        select(func.count()).select_from(ContactRequest).where(ContactRequest.status == "new")
    ).scalar_one()

    total_in_progress = db.execute(
        select(func.count()).select_from(ContactRequest).where(ContactRequest.status == "in_progress")
    ).scalar_one()

    total_resolved = db.execute(
        select(func.count()).select_from(ContactRequest).where(ContactRequest.status == "resolved")
    ).scalar_one()

    return {
        "total_newsletters": total_newsletters,
        "total_new_requests": total_new,
        "total_in_progress": total_in_progress,
        "total_resolved": total_resolved,
    }
