import graphene
import athome.api.schema

class Query(athome.api.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)