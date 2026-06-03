from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func, case

from pydantic import BaseModel
from typing import List

from app.db.session import get_db
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackOut

router = APIRouter(prefix="/feedback", tags=["Feedback"])


# ============================
# RESPONSE SCHEMA
# ============================
class ServiceSummaryOut(BaseModel):
    service: str
    good: int
    neutral: int
    bad: int
    total: int


# ============================
# LIST FEEDBACKS
# ============================
@router.get("", response_model=list[FeedbackOut])
def list_feedbacks(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    stmt = select(Feedback).order_by(Feedback.id.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


# ============================
# SERVICE SUMMARY 
# ============================
@router.get("/service-summary", response_model=List[ServiceSummaryOut])
def feedback_service_summary(db: Session = Depends(get_db)):
    """
    Aggregates feedback per service using rating:
    rating >= 4 -> good
    rating == 3 -> neutral
    rating <= 2 -> bad
    """

    good_case = case((Feedback.rating >= 4, 1), else_=0)
    neutral_case = case((Feedback.rating == 3, 1), else_=0)
    bad_case = case((Feedback.rating <= 2, 1), else_=0)

    stmt = (
        select(
            Feedback.service.label("service"),
            func.sum(good_case).label("good"),
            func.sum(neutral_case).label("neutral"),
            func.sum(bad_case).label("bad"),
            func.count(Feedback.id).label("total"),
        )
        .where(Feedback.service.is_not(None))
        .group_by(Feedback.service)
        .order_by(func.count(Feedback.id).desc())
    )

    rows = db.execute(stmt).all()

    return [
        ServiceSummaryOut(
            service=row.service,
            good=int(row.good or 0),
            neutral=int(row.neutral or 0),
            bad=int(row.bad or 0),
            total=int(row.total or 0),
        )
        for row in rows
    ]


# ============================
# GET SINGLE FEEDBACK
# ============================
@router.get("/{feedback_id}", response_model=FeedbackOut)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    row = db.get(Feedback, feedback_id)
    if not row:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return row


# ============================
# CREATE FEEDBACK
# ============================
@router.post("", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
def create_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    row = Feedback(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


# ============================
# UPDATE FEEDBACK
# ============================
@router.put("/{feedback_id}", response_model=FeedbackOut)
def update_feedback(feedback_id: int, payload: FeedbackUpdate, db: Session = Depends(get_db)):
    row = db.get(Feedback, feedback_id)
    if not row:
        raise HTTPException(status_code=404, detail="Feedback not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(row, k, v)

    db.commit()
    db.refresh(row)
    return row


# ============================
# DELETE FEEDBACK
# ============================
@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    row = db.get(Feedback, feedback_id)
    if not row:
        raise HTTPException(status_code=404, detail="Feedback not found")

    db.delete(row)
    db.commit()
    return None
