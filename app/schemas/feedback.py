from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FeedbackBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)

    role: Optional[str] = Field(None, max_length=120)
    company: Optional[str] = Field(None, max_length=150)

    service: str = Field(..., max_length=120)

    rating: int = Field(..., ge=1, le=5)
    rating_label: str = Field(..., max_length=20)  # good / average / bad

    message: str

    avatar_url: Optional[str] = None
    can_publish: bool = False


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    role: Optional[str] = None
    company: Optional[str] = None

    service: Optional[str] = None

    rating: Optional[int] = None
    rating_label: Optional[str] = None

    message: Optional[str] = None

    avatar_url: Optional[str] = None
    can_publish: Optional[bool] = None

    publish_status: Optional[str] = None
    status: Optional[str] = None
    is_featured: Optional[bool] = None
    note: Optional[str] = None


class FeedbackOut(BaseModel):
    id: int

    first_name: str
    last_name: str

    role: Optional[str]
    company: Optional[str]

    service: str
    rating: int
    rating_label: str

    message: str
    avatar_url: Optional[str]

    can_publish: bool
    publish_status: str
    status: str
    is_featured: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
