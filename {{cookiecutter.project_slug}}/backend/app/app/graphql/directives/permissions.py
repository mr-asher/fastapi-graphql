from jose import jwt

from fastapi import HTTPException, status

from ariadne.schema_visitor import SchemaDirectiveVisitor
from graphql import default_field_resolver
from app import crud, models, database_schemas 
from app.core.config import settings
from app.core import security
from app.graphql.utils import get_context_db


class LoginRequiredDirective(SchemaDirectiveVisitor):

    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        async def resolve_scope(obj, info, **kwargs):

            db = get_context_db(info)

            token = security.get_token_from_auth_header(info.context["request"])

            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
                )
                token_data = database_schemas.TokenPayload(**payload)
            except (jwt.JWTError, jwt.JWTExpiredError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Could not validate credentials",
                )

            user = crud.user.get(db, id=token_data.sub)
            
            if user and user.is_active: 
                return original_resolver(obj, info, **kwargs)

            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this resource",
                )

        field.resolve = resolve_scope

        return field



