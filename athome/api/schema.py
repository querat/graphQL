import  graphene
from    django.db.models            import Model
from    graphene_django             import DjangoObjectType
from    graphene_django.debug       import DjangoDebug
from    athome.api.models           import Module, Sample, User
from    athome.api.mutations.Module import ModuleNode, CreateModule, UpdateModule, AssignModuleToBox
from    athome.api.mutations.Sample import SampleNode, CreateSample
from    athome.api.mutations.User   import UserNode,   CreateUser
from    athome.api.mutations.Box    import BoxNode,    CreateBox   , AssignBoxToUser


class Query(object):
    debug           = graphene.Field(DjangoDebug)
    allModules      = graphene.List(ModuleNode)
    allSamples      = graphene.List(SampleNode)
    allUsers        = graphene.List(UserNode)
    getModuleById   = graphene.Field(ModuleNode, moduleId=graphene.Int())

    def resolve_allModules(self, info, **kwargs):
        return Module.objects.all()

    def resolve_allSamples(self, info, **kwargs):
        return Sample.objects.all().order_by(Sample.date)

    def resolve_getModuleById(self, info, **kwargs):
        return ModuleNode.get_node(info, kwargs.get("moduleId"))

    def resolve_allUsers(self, info, **kwargs):
        return User.objects.all() # .order_by(User.id)


class Mutation(object):
    createModule        = CreateModule.Field()
    updateModule        = UpdateModule.Field()
    assignModuleToBox   = AssignModuleToBox.Field()

    createSample        = CreateSample.Field()

    createUser          = CreateUser.Field()

    createBox           = CreateBox.Field()
    assignBoxToUser     = AssignBoxToUser.Field()

    debug               = graphene.Field(DjangoDebug)