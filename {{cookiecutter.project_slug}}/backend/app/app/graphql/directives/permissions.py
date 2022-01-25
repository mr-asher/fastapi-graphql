from jose import jwt

from fastapi import HTTPException, status

from ariadne.schema_visitor import SchemaDirectiveVisitor
from graphql import default_field_resolver
from app.core.config import settings
from app.core import security


class PermissionsDirective(SchemaDirectiveVisitor):

    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        async def resolve_scope(obj, info, **kwargs):

            headers = info.context["request"]["headers"]

            authorization_header = [
                header for header in headers if b"authorization" in header
            ]

            if not authorization_header:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No authorization token"
                )

            _, _, token = authorization_header[0][1].decode("utf-8").partition(" ")

            authorized = True

            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
                )
            except (jwt.JWTError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Could not validate credentials",
                )

            if authorized:
                return original_resolver(obj, info, **kwargs)

            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this resource",
                )

        field.resolve = resolve_scope

        return field

