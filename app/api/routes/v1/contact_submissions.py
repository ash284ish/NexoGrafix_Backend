from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.contact_requests import ContactRequest
from app.schemas.contact_request import ContactRequestCreate, ContactRequestUpdate, ContactRequestOut

router = APIRouter(prefix="/contact-requests", tags=["Contact Requests"])


@router.get("", response_model=list[ContactRequestOut])
def list_contact_submissions(db: Session = Depends(get_db), limit: int = 50, offset: int = 0, status_filter: str | None = None):
    stmt = select(ContactRequest).order_by(ContactRequest.id.desc()).limit(limit).offset(offset)
    if status_filter:
        stmt = stmt.where(ContactRequest.status == status_filter)
    return db.execute(stmt).scalars().all()


@router.get("/{request_id}", response_model=ContactRequestOut)
def get_contact_request(request_id: int, db: Session = Depends(get_db)):
    row = db.get(ContactRequest, request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Contact request not found")
    return row


@router.post("", response_model=ContactRequestOut, status_code=status.HTTP_201_CREATED)
def create_contact_request(payload: ContactRequestCreate, db: Session = Depends(get_db)):
    row = ContactRequest(
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=str(payload.email).strip().lower(),
        phone=(payload.phone.strip() if payload.phone else None),
        service=(payload.service.strip() if payload.service else None),
        message=payload.message.strip(),
        note=(payload.note.strip() if payload.note else None),
        status="new",
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.patch("/{request_id}", response_model=ContactRequestOut)
def update_contact_request(request_id: int, payload: ContactRequestUpdate, db: Session = Depends(get_db)):
    row = db.get(ContactRequest, request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Contact request not found")

    if payload.first_name is not None:
        row.first_name = payload.first_name.strip()
    if payload.last_name is not None:
        row.last_name = payload.last_name.strip()
    if payload.email is not None:
        row.email = str(payload.email).strip().lower()
    if payload.phone is not None:
        row.phone = payload.phone.strip() if payload.phone else None
    if payload.service is not None:
        row.service = payload.service.strip() if payload.service else None
    if payload.message is not None:
        row.message = payload.message.strip()
    if payload.status is not None:
        row.status = payload.status
    if payload.note is not None:
        row.note = payload.note.strip() if payload.note else None

    db.commit()
    db.refresh(row)
    return row


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_request(request_id: int, db: Session = Depends(get_db)):
    row = db.get(ContactRequest, request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Contact request not found")
    db.delete(row)
    db.commit()
    return
