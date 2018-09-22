import graphene
import graphql
from athome.api.models.Module               import Module
from athome.api.models.Threshold            import Threshold
from athome.api.mutations.nodes.Threshold   import ThresholdNode


class ThresholdInput(graphene.InputObjectType):
    name        = graphene.String()
    default     = graphene.Int()
    min         = graphene.Int()
    max         = graphene.Int()
    current     = graphene.Int()
    moduleId    = graphene.ID()

class CreateThreshold(graphene.Mutation):

    class Arguments:
        thresholdInput = graphene.Argument(ThresholdInput)

    threshold = graphene.Field(ThresholdNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        threshold = Threshold()
        thresholdInput = kwargs.get("thresholdInput")

        for inputArg in ["name", "default", "min", "max", "current", "moduleId"]:
            setattr(threshold, inputArg, getattr(thresholdInput, inputArg))


        moduleIdOfThreshold = thresholdInput["moduleId"]
        moduleOfThreshold = Module.objects.filter(id=moduleIdOfThreshold).first()
        if moduleOfThreshold is None:
            raise graphql.GraphQLError("module #{} does not exist !".format(moduleIdOfThreshold))

        threshold.save(force_insert=True)
        return CreateThreshold(threshold=threshold)
