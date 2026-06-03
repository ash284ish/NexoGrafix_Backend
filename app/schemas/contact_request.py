from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal


ContactStatus = Literal["new", "in_progress", "resolved", "spam"]


class ContactRequestCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=30)
    service: Optional[str] = Field(default=None, max_length=120)
    message: str = Field(min_length=1)
    note: Optional[str] = None


class ContactRequestUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=30)
    service: Optional[str] = Field(default=None, max_length=120)
    message: Optional[str] = None
    status: Optional[ContactStatus] = None
    note: Optional[str] = None


class ContactRequestOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str]
    service: Optional[str]
    message: str
    status: str
    note: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
