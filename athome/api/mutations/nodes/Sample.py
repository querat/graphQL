from graphene_django import DjangoObjectType

from athome.api.models.Sample import Sample


class SampleNode(DjangoObjectType):
    def resolve_id(self, info):
        return self.id
    class Meta:
        model = Sample