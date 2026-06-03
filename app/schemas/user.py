from pydantic import BaseModel, EmailStr
from typing import Optional


class UserOut(BaseModel):
    id: int
    role_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    role_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    is_active: bool = True


class UserUpdate(BaseModel):
    role_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserLogin(BaseModel):
    phone: str
    password: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ChangePasswordIn(BaseModel):
    old_password: str
    new_password: str
