import graphene
from graphene_django    import DjangoObjectType
from athome.api.models  import Sample

from athome.api.models.Module  import Module

class SampleNode(DjangoObjectType):
    class Meta:
        model = Sample


class SampleInput(graphene.InputObjectType):
    payload         = graphene.String()
    date            = graphene.String()
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


