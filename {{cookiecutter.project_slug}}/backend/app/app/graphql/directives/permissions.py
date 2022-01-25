from jose import jwt

from ariadne.schema_visitor import SchemaDirectiveVisitor
from ariadne.exceptions import HttpBadRequestError
from graphql import default_field_resolver
from app.core.config import settings
from app.core import security


class PermissionsDirective(SchemaDirectiveVisitor):

    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        async def resolve_scope(obj, info, **kwargs):
            authorization_header = [
                header for header in info.context["request"]["headers"] if b"authorization" in header
            ]

            _, _, token = authorization_header[0][1].decode("utf-8").partition(" ")

            authorized = False

            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )

            print(payload)

            if authorized:
                return await original_resolver(obj, info, **kwargs)

            raise HttpBadRequestError("User not authorized for resource")

        field.resolve = resolve_scope

        return field

