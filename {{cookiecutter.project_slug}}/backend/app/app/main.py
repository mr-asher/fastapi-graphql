from ariadne import QueryType, make_executable_schema, load_schema_from_path, ObjectType
from ariadne.asgi import GraphQL

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings


type_definitions = load_schema_from_path("/app/app/graphql-schemas/")

query = QueryType()

@query.field("healthCheck")
def resolve_health_check(*_):
    return { "ok": True }

schema = make_executable_schema(type_definitions, query)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_route("/graphql", GraphQL(schema, debug=True)) 
app.add_websocket_route("/graphql", GraphQL(schema, debug=True)) 
