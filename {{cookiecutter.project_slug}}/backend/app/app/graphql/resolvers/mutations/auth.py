import datetime

from ariadne import MutationType
from fastapi import HTTPException 
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import User

from app.db.session import SessionLocal

from app.core import security

mutation = MutationType()

@mutation.field("tokenAuth")
async def resolve_token_auth(obj, info, username, password):
    db = SessionLocal()
    user = crud.user.authenticate(db, email=username, password=password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {"token": token}
