from graphene_django    import DjangoObjectType
from athome.api.models  import Sample

class SampleNode(DjangoObjectType):
    class Meta:
        model = Sample
