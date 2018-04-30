import  graphene
from    django.db.models            import Model
from    graphene_django             import DjangoObjectType
from    graphene_django.debug       import DjangoDebug
from    athome.api.models           import Module, Sample
from    athome.api.mutations.Module import ModuleNode, CreateModule, UpdateModule
from    athome.api.mutations.Sample import SampleNode, CreateSample

class Query(object):
    debug           = graphene.Field(DjangoDebug)
    allModules      = graphene.List(ModuleNode)
    allSamples      = graphene.List(SampleNode)
    getModuleById   = graphene.Field(ModuleNode, moduleId=graphene.Int())

    def resolve_allModules(self, info, **kwargs):
        return Module.objects.all()

    def resolve_allSamples(self, info, **kwargs):
        return Sample.objects.all().order_by(Sample.date)

    def resolve_getModuleById(self, info, **kwargs):
        return ModuleNode.get_node(info, kwargs.get("moduleId"))


class Mutation(object):
    createModule        = CreateModule.Field()
    updateModule        = UpdateModule.Field()
    createSample        = CreateSample.Field()
    debug               = graphene.Field(DjangoDebug)