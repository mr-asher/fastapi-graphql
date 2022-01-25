from ariadne import QueryType

query = QueryType()

@query.field("healthCheck")
def resolve_health_check(*_):
    return { "ok": True }


@query.field("checkAuthToken")
def resolve_check_auth_token(*_):
    return { "ok": True }

