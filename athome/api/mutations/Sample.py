import graphene
import graphql
from athome.api.models.Sample   import Sample
from athome.api.models.Box      import Box
from athome.api.models.Module   import Module
from athome.api.mutations.nodes.Sample import SampleNode


class SampleInput(graphene.InputObjectType):
    payload         = graphene.String()
    date            = graphene.DateTime()
    moduleId        = graphene.ID()


class CreateSample(graphene.Mutation):
    class Arguments:
        sampleInput = graphene.Argument(SampleInput)

    sample = graphene.Field(SampleNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        sampleInput = kwargs.get("sampleInput")
        newSample = Sample(
            module      = Module.objects.get(pk=sampleInput.moduleId)
            , date      = sampleInput.date
            , payload   = sampleInput.payload
        )
        newSample.save(force_insert=True)
        return CreateSample(sample=newSample)


class SendSamples(graphene.Mutation):
    class Arguments:
        boxId       = graphene.ID()
        boxAuthCode = graphene.String()
        samples     = graphene.List(SampleInput)

    nbSentSamples = graphene.Field(graphene.Int)

    @staticmethod
    def mutate(root, info, **kwargs):
        boxId           = kwargs.get("boxId")
        boxAuthCode     = kwargs.get("boxAuthCode")
        sampleInputs    = kwargs.get("samples")
        box             = None

        try:
            box = Box.objects.get(pk=boxId)
        except Box.DoesNotExist:
            raise graphql.GraphQLError("Box #{} does not exist".format(boxId))

        if box.authCode != boxAuthCode:
            raise graphql.GraphQLError("Invalid box authentication code")

        nbSentSamples = 0
        for sampleInput in sampleInputs:
            dbSample        = Sample()
            sampleModule    = None
            try:
                sampleModule = Module.objects.get(pk=sampleInput.moduleId)
            except:
                raise graphql.GraphQLError("module #{} does not exist".format(sampleInput.moduleId))
            [setattr(dbSample, key, value) for key, value in sampleInput.items()]
            dbSample.module = sampleModule
            dbSample.save(force_insert=True)
            nbSentSamples += 1

        return SendSamples(nbSentSamples=nbSentSamples)

