from app.graphql.directives import directives
from ariadne import make_executable_schema, load_schema_from_path
from app.graphql.resolvers.queries import query
from app.graphql.resolvers.mutations import mutation

type_definitions = load_schema_from_path("/app/app/graphql")


schema = make_executable_schema(type_definitions, query, mutation, directives=directives)
