import  graphene
import  graphene_django
from    graphene_django     import DjangoObjectType
from    athome.api.models   import Module, Sample

print(graphene.__version__)

class ModuleNode(DjangoObjectType):

    def resolve_id(self, info):
        return self.id

    class Meta:
        model = Module

class SampleNode(DjangoObjectType):
    class Meta:
        model = Sample

class Query(object):
    allModules      = graphene.List(ModuleNode)
    allSamples      = graphene.List(SampleNode)
    getModuleById   = graphene.Field(ModuleNode, moduleId=graphene.Int())

    def resolve_allModules(self, info, **kwargs):
        return Module.objects.all()

    def resolve_allSamples(self, info, **kwargs):
        return Sample.objects.all()

    def resolve_getModuleById(self, info, **kwargs):
        return ModuleNode.get_node(info, kwargs.get("moduleId"))


class ModuleInput(graphene.InputObjectType):
    mac             = graphene.String(required=True)
    name            = graphene.String(required=True)
    location        = graphene.String(required=True)
    type            = graphene.String(required=True)
    vendor          = graphene.String(required=True)


class CreateLol(graphene.Mutation):
    class Arguments:
        lol = graphene.String()

    lol = graphene.Field(lambda: graphene.String)

    def mutate(self, info, lol):
        return CreateLol(lol=lol)


class CreateModule(graphene.Mutation):
    class Input:
        module      = graphene.Argument(ModuleInput)

    module = graphene.Field(ModuleNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        input = kwargs.get("module")

        module = ModuleNode(
            mac         = input.mac
            , name      = input.name
            , location  = input.location
            , type      = input.type
            , vendor    = input.vendor
        )

        return CreateModule(module=module)

class Mutation(object):
    createModule        = CreateModule.Field()
    createlol           = CreateLol.Field()

