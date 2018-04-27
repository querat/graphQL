import  graphene
import  graphene_django
from    graphene_django import DjangoObjectType
from    athome.api.models import Module, Sample


class ModuleType(DjangoObjectType):
    class Meta:
        model = Module

class SampleType(DjangoObjectType):
    class Meta:
        model = Sample


class Query(object):
    allModules      = graphene.List(ModuleType)
    allSamples      = graphene.List(SampleType)
    getModuleById   = graphene.Field(ModuleType, moduleId=graphene.Int())

    def resolve_allModules(self, info, **kwargs):
        return Module.objects.all()

    def resolve_allSamples(self, info, **kwargs):
        return Sample.objects.all()

    def resolve_getModuleById(self, info, **kwargs):
        return ModuleType.get_node(info, kwargs.get("moduleId"))


