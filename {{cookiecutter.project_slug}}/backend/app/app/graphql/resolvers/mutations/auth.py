import datetime

from ariadne import MutationType
from fastapi import HTTPException

from app import crud
from app.core.config import settings
from app.graphql.utils import get_context_db

from app.core import security

mutation = MutationType()

@mutation.field("tokenAuth")
async def resolve_token_auth(obj, info, input):
    db = get_context_db(info)
    user = crud.user.authenticate(db, email=input["username"], password=input["password"])

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