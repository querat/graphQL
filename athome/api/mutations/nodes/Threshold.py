import  graphene
import  graphene_django
from    graphene_django             import DjangoObjectType
from    athome.api.models.Threshold import Threshold

class NewThreshold(graphene.Mutation):
    class Arguments:
        lol = graphene.Int()

    xD = graphene.Int()

    @staticmethod
    def mutate(root, info, **kwargs):
        return 42


class ThresholdNode(DjangoObjectType):
    class Meta:
        model = Threshold
