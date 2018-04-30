import graphene
from graphene_django    import DjangoObjectType
from athome.api.models  import Module

class ModuleNode(DjangoObjectType):
    def resolve_id(self, info):
        return self.id

    class Meta:
        model = Module


class ModuleInput(graphene.InputObjectType):
    mac             = graphene.String()
    name            = graphene.String()
    location        = graphene.String()
    type            = graphene.String()
    vendor          = graphene.String()


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


class UpdateModule(graphene.Mutation):

    module = graphene.Field(ModuleNode)

    class Arguments:
        moduleInput = graphene.Argument(ModuleInput)
        moduleId    = graphene.Argument(graphene.ID)

    @staticmethod
    def mutate(root, info, **kwargs):
        moduleInput = kwargs.get("moduleInput")
        moduleId = kwargs.get("moduleId")
        toUpdate = Module.objects.get(pk=moduleId)

        [setattr(toUpdate, key, value) for key, value in moduleInput.items()]

        toUpdate.save(force_update=True)
        return UpdateModule(module=toUpdate)
