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

        requiredArgs = ["name", "default", "min", "max", "current"]
        for requiredArgKey in requiredArgs:
            valueFromInput = getattr(thresholdInput, requiredArgKey)
            if valueFromInput is None:
                raise graphql.GraphQLError(f"Missing argument: {requiredArgKey}")
            setattr(threshold, requiredArgKey, valueFromInput)

        moduleIdOfThreshold = thresholdInput.get("moduleId")
        if moduleIdOfThreshold is None:
            raise graphql.GraphQLError(f"Missing argument: moduleId")
        moduleOfThreshold = Module.objects.filter(id=moduleIdOfThreshold).first()
        if moduleOfThreshold is None:
            raise graphql.GraphQLError("module #{} does not exist !".format(moduleIdOfThreshold))
        threshold.module = moduleOfThreshold

        threshold.save(force_insert=True)
        return CreateThreshold(threshold=threshold)


class UpdateThreshold(graphene.Mutation):

    class Arguments:
        thresholdId     = graphene.Argument(graphene.ID)
        thresholdInput  = graphene.Argument(ThresholdInput)

    threshold = graphene.Field(ThresholdNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        threshold      = Threshold()
        thresholdInput = kwargs.get("thresholdInput")
        thresholdId    = kwargs.get("thresholdId")

        if thresholdId is None:
            raise graphql.GraphQLError("Missing argument: thresholdId")
        threshold = Threshold.objects.filter(id=thresholdId).first()
        if threshold is None:
            raise graphql.GraphQLError(f"threshold with id {thresholdId} not found")

        args = ["name", "default", "min", "max", "current", "moduleId"]
        for arg in args:
            valueFromInput = getattr(thresholdInput, arg)
            if valueFromInput is not None:
                setattr(threshold, arg, valueFromInput)

        moduleIdOfThreshold = thresholdInput.get("moduleId")
        if moduleIdOfThreshold is not None:
            moduleOfThreshold = Module.objects.filter(id=moduleIdOfThreshold).first()
            if moduleOfThreshold is None:
                raise graphql.GraphQLError("module #{} does not exist !".format(moduleIdOfThreshold))
            threshold.module = moduleOfThreshold

        threshold.save(force_update=True)
        return UpdateThreshold(threshold=threshold)
