from typing import Any, Dict
from ariadne.asgi import GraphQL

from fastapi_jwt_auth import AuthJWT 
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Depends 
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.datastructures import URL

from sqlalchemy.orm import Session

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.graphql.schema import schema
from app.api import deps

GraphQLContext = Dict[str, Any]

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

# Add REST API routes. 
app.include_router(api_router, prefix=settings.API_V1_STR)

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# Setup Graphql Connection

# Manage context for graphql and provide access to database and request from resolvers.
# This allows access to the database session via dependencies just like normal API routes. 
# Use info.context["request"]["state"]["db"]
async def get_graphql_context(request: Request, db: Session) -> GraphQLContext:
    return {"request": request, "db": db}

async def resolve_graphql_context(request: Request) -> GraphQLContext:
    return await get_graphql_context(request, request["state"]["db"])

graphql = GraphQL(schema, debug=True)

app.mount("/graphql/", graphql)

@app.get("/graphql")
async def graphiql(request: Request):
    request._url = URL("/graphql")
    return await graphql.render_playground(request=request)

@app.post("/graphql")
async def graphql_post(request: Request, db: Session = Depends(deps.get_db), authorize: AuthJWT = Depends()):
    request.state.db = db
    request.state.authorize = authorize
    return await graphql.graphql_http_server(request=request)

app.add_websocket_route("/graphql", GraphQL(schema, debug=True)) 

