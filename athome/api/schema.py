import  graphene
from    graphene_django         import DjangoObjectType
from    graphene_django.debug   import DjangoDebug
from    athome.api.models       import Module, Sample

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
    mac             = graphene.String()
    name            = graphene.String()
    location        = graphene.String()
    type            = graphene.String()
    vendor          = graphene.String()


class UpdateModule(graphene.Mutation):
    class Arguments:
        moduleInput = graphene.Argument(ModuleInput)
        moduleId    = graphene.Argument(graphene.ID)

    module      = graphene.Field(ModuleNode)
    # id          = graphene.Field(graphene.Int)

    @staticmethod
    def mutate(root, info, **kwargs):
        moduleInput = kwargs.get("moduleInput")
        moduleId    = kwargs.get("moduleId")
        toUpdate    = Module.objects.get(pk=moduleId)

        [setattr(toUpdate, key, value) for key, value in moduleInput.items()]

        toUpdate.save(force_update=True)
        return UpdateModule(module=toUpdate)


class CreateModule(graphene.Mutation):
    class Arguments:
        moduleInput = graphene.Argument(ModuleInput)

    module = graphene.Field(ModuleNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        moduleInput = kwargs.get("moduleInput")
        dbModule = Module(
            mac         = moduleInput.mac
            , name      = moduleInput.name
            , location  = moduleInput.location
            , type      = moduleInput.type
            , vendor    = moduleInput.vendor
        )
        dbModule.save(force_insert=True)
        return CreateModule(module=dbModule)


class Mutation(object):
    createModule        = CreateModule.Field()
    updateModule        = UpdateModule.Field()
    __debug             = graphene.Field(DjangoDebug)