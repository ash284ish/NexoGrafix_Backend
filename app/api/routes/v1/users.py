from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserLogin, LoginOut, ChangePasswordIn
from app.core.security import get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["Users"])


def _get_current_user(db: Session, authorization: str | None):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.split(" ", 1)[1].strip()
    if not token.startswith("user:"):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_id = int(token.split(":", 1)[1])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    return user


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    stmt = select(User).order_by(User.id.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    row = db.get(User, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return row


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    email = str(payload.email).strip().lower()

    exists = db.execute(select(User.id).where(User.email == email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")

    row = User(
        role_id=payload.role_id,
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=email,
        phone=(payload.phone.strip() if payload.phone else None),
        password_hash=get_password_hash(payload.password),
        is_active=payload.is_active,
    )

    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.post("/login", response_model=LoginOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    phone = payload.phone.strip()

    user = db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = f"user:{user.id}"
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    return {"message": "Logged out successfully"}


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    payload: ChangePasswordIn,
    db: Session = Depends(get_db),
    authorization: str | None = Header(default=None),
):
    user = _get_current_user(db, authorization)

    if not verify_password(payload.old_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid old password")

    new_pwd = payload.new_password.strip()
    if len(new_pwd) < 6:
        raise HTTPException(status_code=400, detail="Password too short")

    user.password_hash = get_password_hash(new_pwd)
    db.commit()

    return {"message": "Password updated successfully"}


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    row = db.get(User, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.first_name is not None:
        row.first_name = payload.first_name.strip()
    if payload.last_name is not None:
        row.last_name = payload.last_name.strip()
    if payload.email is not None:
        row.email = str(payload.email).strip().lower()
    if payload.phone is not None:
        row.phone = payload.phone.strip() if payload.phone else None
    if payload.role_id is not None:
        row.role_id = payload.role_id
    if payload.is_active is not None:
        row.is_active = payload.is_active

    db.commit()
    db.refresh(row)
    return row


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    row = db.get(User, user_id)
    if not row:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(row)
    db.commit()
    return
