from graphene_django                import DjangoObjectType
from athome.api.models.Threshold    import Threshold

class ThresholdNode(DjangoObjectType):
    class Meta:
        model = Threshold
