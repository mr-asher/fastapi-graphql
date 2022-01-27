from typing import Generator

from fastapi import Depends, HTTPException 
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud, models 
from app.db.session import SessionLocal

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), 
    Authorize: AuthJWT = Depends() 
) -> models.User:
    Authorize.jwt_required()
    user = crud.user.get(db, id=Authorize.get_jwt_subject())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
