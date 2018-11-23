import graphene
import graphql
from graphql                            import GraphQLError

from athome.api.models.Module           import Module
from athome.api.models.Box              import Box
from athome.api.mutations.nodes.Module  import ModuleNode


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
            , authCode="authCodeHashHere" # TODO generate password
        )
        dbModule.save(force_insert=True)
        return CreateModule(module=dbModule)


class UpdateModule(graphene.Mutation):
    module = graphene.Field(ModuleNode)

    class Arguments:
        moduleInput = graphene.Argument(ModuleInput)
        moduleId = graphene.Argument(graphene.ID)
        moduleAuthCode = graphene.Argument(graphene.String)


    @staticmethod
    def mutate(root, info, **kwargs):
        moduleInput     = kwargs.get("moduleInput")
        moduleId        = kwargs.get("moduleId")
        moduleAuthCode  = kwargs.get("moduleAuthCode")

        if moduleId is None:
            raise GraphQLError("No moduleId Provided")

        moduleToUpdate  = Module.objects.filter(pk=moduleId).first()
        if moduleToUpdate is None:
            raise GraphQLError(f"Module #{moduleId}")

        if moduleAuthCode is None:
            raise GraphQLError(f"No authCode provided for module #{moduleId}")
        if moduleToUpdate.authCode != moduleAuthCode:
            raise GraphQLError(f"Invalid credentials provided for module {moduleId}")

        [setattr(moduleToUpdate, key, value) for key, value in moduleInput.items()]

        moduleToUpdate.save(force_update=True)
        return UpdateModule(module=moduleToUpdate)


class AssignModuleToBox(graphene.Mutation):

    class Arguments:
        moduleId        = graphene.Argument(graphene.ID)
        boxId           = graphene.Argument(graphene.ID)
        boxAuthCode     = graphene.Argument(graphene.String)
        moduleAuthCode  = graphene.Argument(graphene.String)

    module = graphene.Field(ModuleNode)

    @staticmethod
    def mutate(root, info, **kwargs):

        requiredArgs = ["moduleId", "boxId", "boxAuthCode", "moduleAuthCode"]
        for requiredArg in requiredArgs:
            if kwargs.get(requiredArg)is None:
                raise GraphQLError(f"missing argument: {requiredArg}")

        affectedModule = Module.objects.filter(pk=kwargs["moduleId"]).first()
        if affectedModule is None:
            raise graphql.GraphQLError("Module #{} does not exist".format(kwargs["moduleId"]))

        if affectedModule.authCode != kwargs["moduleAuthCode"]:
            raise GraphQLError(f"Invalid auth code provided for module #{kwargs['moduleId']}")

        box = Box.objects.filter(pk=kwargs["boxId"]).first()
        if box is None:
            raise graphql.GraphQLError(f"Box #{kwargs['boxId']} does not exist")

        if box.authCode != kwargs["boxAuthCode"]:
            raise graphql.GraphQLError(f"Invalid auth code provided for box {kwargs['boxId']}")

        affectedModule.box = box
        affectedModule.save(force_update=True)

        return AssignModuleToBox(module=affectedModule)
