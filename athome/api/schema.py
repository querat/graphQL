import  graphene
from    graphene_django import DjangoObjectType
from    athome.api.models import Module

class ModuleType(DjangoObjectType):
    class Meta:
        model = Module

class Query(object):
    allModules = graphene.List(ModuleType)

    def resolve_allModules(self, info, **kwargs):
        return Module.objects.all()