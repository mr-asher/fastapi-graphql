import datetime

from ariadne import MutationType
from fastapi import HTTPException

from app.database import crud
from app.core.config import settings
from app.graphql.utils import get_context_db, get_authorize

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

    token = get_authorize(info).create_access_token(subject=user.id)
    return {"token": token}
