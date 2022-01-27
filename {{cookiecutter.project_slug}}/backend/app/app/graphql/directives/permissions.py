from ariadne.schema_visitor import SchemaDirectiveVisitor
from graphql import default_field_resolver
from app.graphql.utils import get_authorize


class LoginRequiredDirective(SchemaDirectiveVisitor):

    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        async def resolve_scope(obj, info, **kwargs):
            get_authorize(info).jwt_required()
            return original_resolver(obj, info, **kwargs)

        field.resolve = resolve_scope

        return field



