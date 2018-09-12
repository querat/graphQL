import  bcrypt
import  graphene
import  graphql
from    django.db.models            import Model
from    graphene_django             import DjangoObjectType
from    graphene_django.debug       import DjangoDebug
from    athome.api.models           import Module, Sample

from    athome.api.models.User      import User
from    athome.api.mutations.Module import Module, ModuleNode, CreateModule, UpdateModule, AssignModuleToBox
from    athome.api.mutations.Sample import Sample, SampleNode, CreateSample, SendSamples
from    athome.api.mutations.User   import User, UserNode,   CreateUser
from    athome.api.mutations.Box    import Box, BoxNode,    CreateBox   , AssignBoxToUser


class Query(object):
    debug           = graphene.Field(DjangoDebug)
    allModules      = graphene.List(ModuleNode)
    allSamples      = graphene.List(SampleNode)
    allBoxes        = graphene.List(BoxNode)
    allUsers        = graphene.List(UserNode)
    getModuleById   = graphene.Field(ModuleNode, moduleId=graphene.Int())

    getUser         = graphene.Field(
        UserNode
        , userName  = graphene.String()
        , password  = graphene.String()
    )

    getBoxById      = graphene.Field(
        BoxNode
        , boxId       = graphene.ID()
        , boxAuthCode = graphene.String()
    )

    def resolve_getUser(self, info, **kwargs):
        userName = kwargs.get("userName")
        password = kwargs.get("password")
        user     = None

        try:
            user = User.objects.get(name=userName)
        except User.DoesNotExist:
            raise graphql.GraphQLError("User '{}' not found".format(userName))
        if not bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
            raise graphql.GraphQLError("invalid password for User '{}'".format(userName))
        return user

    def resolve_getBoxById(self, _, **kwargs):
        boxId       = kwargs.get("boxId")
        authCode    = kwargs.get("boxAuthCode")
        box         = None

        try:
            box = Box.objects.get(pk=boxId)
        except Box.DoesNotExist:
            raise graphql.GraphQLError("box #{} does not exist".format(boxId))
        if authCode != box.authCode:
            raise graphql.GraphQLError("invalid authcode for box #".format(boxId))
        return box

    def resolve_allBoxes(self, _, **kwargs):
        return Box.objects.all()

    def resolve_allModules(self, _, **kwargs):
        return Module.objects.all()

    def resolve_allSamples(self, _, **kwargs):
        return Sample.objects.all().order_by('date')

    def resolve_getModuleById(self, info, **kwargs):
        return ModuleNode.get_node(info, kwargs.get("moduleId"))

    def resolve_allUsers(self, info, **kwargs):
        return User.objects.all() # .order_by(User.id)



class Mutation(object):
    debug               = graphene.Field(DjangoDebug)

    createUser          = CreateUser.Field()

    createBox           = CreateBox.Field()
    assignBoxToUser     = AssignBoxToUser.Field()

    createModule        = CreateModule.Field()
    updateModule        = UpdateModule.Field()
    assignModuleToBox   = AssignModuleToBox.Field()

    createSample        = CreateSample.Field()
    sendSamples         = SendSamples.Field()



