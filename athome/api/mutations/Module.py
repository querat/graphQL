import graphene
import graphql
from graphene_django            import DjangoObjectType
from athome.api.models.Module   import Module
from athome.api.models.Box      import Box


class ModuleNode(DjangoObjectType):
    def resolve_id(self, info):
        return self.id

    class Meta:
        model = Module


class ModuleInput(graphene.InputObjectType):
    mac = graphene.String()
    name = graphene.String()
    location = graphene.String()
    type = graphene.String()
    vendor = graphene.String()


class CreateModule(graphene.Mutation):
    class Arguments:
        moduleInput = graphene.Argument(ModuleInput)

    module = graphene.Field(ModuleNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        moduleInput = kwargs.get("moduleInput")
        dbModule = Module(
            mac=moduleInput.mac
            , name=moduleInput.name
            , location=moduleInput.location
            , type=moduleInput.type
            , vendor=moduleInput.vendor
        )
        dbModule.save(force_insert=True)
        return CreateModule(module=dbModule)


class UpdateModule(graphene.Mutation):
    module = graphene.Field(ModuleNode)

    class Arguments:
        moduleInput = graphene.Argument(ModuleInput)
        moduleId = graphene.Argument(graphene.ID)

    @staticmethod
    def mutate(root, info, **kwargs):
        moduleInput = kwargs.get("moduleInput")
        moduleId = kwargs.get("moduleId")
        toUpdate = Module.objects.get(pk=moduleId)

        [setattr(toUpdate, key, value) for key, value in moduleInput.items()]

        toUpdate.save(force_update=True)
        return UpdateModule(module=toUpdate)


class AssignModuleToBox(graphene.Mutation):
    module = graphene.Field(ModuleNode)

    class Arguments:
        moduleId    = graphene.Argument(graphene.ID)
        boxId       = graphene.Argument(graphene.ID)
        boxAuthCode = graphene.Argument(graphene.String)

    @staticmethod
    def mutate(root, info, **kwargs):
        moduleId        = kwargs.get("moduleId")
        boxId           = kwargs.get("boxId")
        boxAuthCode     = kwargs.get("boxAuthCode")

        affectedModule  = None
        box             = None

        try:
            affectedModule = Module.objects.get(pk=moduleId)
        except Module.DoesNotExist:
            raise graphql.GraphQLError("Module #{} does not exist".format(moduleId))
        try:
            box = Box.objects.get(pk=boxId)
        except Box.DoesNotExist:
            raise graphql.GraphQLError("Box #{} does not exist".format(boxId))

        if box.authCode != boxAuthCode:
            raise graphql.GraphQLError("Invalid box authentication code")

        affectedModule.box = box
        affectedModule.save(force_update=True)

        return AssignModuleToBox(module=affectedModule)
