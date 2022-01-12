from ariadne import QueryType

query = QueryType()

@query.field("healthCheck")
def resolve_health_check(*_):
    return { "ok": True }
