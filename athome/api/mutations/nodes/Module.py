import graphene
from graphene_django import DjangoObjectType

from athome.api.models.Module           import Module
from athome.api.models.Sample           import Sample
from athome.api.mutations.nodes.Sample  import SampleNode
from athome.api.mutations.Threshold     import ThresholdNode
from athome.api.mutations.nodes.Threshold import NewThreshold

class ModuleNode(DjangoObjectType):
    class Meta:
        model = Module

    def resolve_id(self, info):
        return self.id

    def resolve_samples(self, info, **kwargs):
        return self.samples

    pootis = graphene.Field(SampleNode, pootis=graphene.ID())

    def resolve_pootis(self, info, **kwargs):
        pootisId = None
        try:
            pootisId = kwargs.get("pootis")
        except Exception as e:
            return None

        return Sample.objects.get(id=pootisId)


    newThreshold = NewThreshold.Field()
    def resolve_newThreshold(self, *args, **kwargs):
        NewThreshold.mutate()