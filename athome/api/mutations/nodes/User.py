from graphene_django import DjangoObjectType

from athome.api.models.User import User


class UserNode(DjangoObjectType):
    def resolve_id(self, info):
        return self.id

    class Meta:
        model = User