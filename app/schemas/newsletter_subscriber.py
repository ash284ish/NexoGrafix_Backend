from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Literal

StatusType = Literal["active", "unsubscribed"]


class NewsletterSubscriberCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status: StatusType = "active"


class NewsletterSubscriberUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    status: StatusType | None = None


class NewsletterSubscriberOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    status: StatusType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
