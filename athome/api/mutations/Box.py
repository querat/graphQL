import  graphene
from    graphql                     import GraphQLError
from    graphene_django             import DjangoObjectType
from    athome.api.models.Box       import Box
from    athome.api.models.User      import User
# from    athome.api.mutations.Module import ModuleNode

from athome.api.models.Box  import Box

class BoxNode(DjangoObjectType):
    class Meta:
        model = Box

    # It is important that a box can access its user's data
    # But not their confidential data
    def resolve_user(self, info, **kwargs):
        if self.user is None:
            return None
        self.user.password = "[private]"
        return self.user

    getModulesByType = graphene.List(ModuleNode, type=graphene.String())
    def resolve_getModuleByType(self, info, **kwargs):
        return 42
        pass

class BoxInput(graphene.InputObjectType):
    userId = graphene.ID()


class AssignBoxToUser(graphene.Mutation):
    class Arguments:
        userName    = graphene.Argument(graphene.String)
        boxId       = graphene.Argument(graphene.ID)
        boxAuthCode = graphene.Argument(graphene.String)

    box = graphene.Field(BoxNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        user        = kwargs.get("userName")
        box         = kwargs.get("boxId")
        auth        = kwargs.get("boxAuthCode")
        newOwner    = None
        modifiedBox = Box.objects.get(id=box)

        try:
            newOwner = User.objects.get(name=user)
        except User.DoesNotExist:
            raise GraphQLError("User '%s' does not exist" % user)

        # Box does not exist
        if modifiedBox is None:
            raise GraphQLError("Box does not exist")

        # Invalid auth code
        if modifiedBox.authCode != auth:
            raise GraphQLError("Invalid authentication code")

        modifiedBox.user = newOwner
        modifiedBox.save(force_update=True)

        return AssignBoxToUser(box=modifiedBox)


class CreateBox(graphene.Mutation):

    box = graphene.Field(BoxNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        newBox = Box(
            user = None              # No user owns the box at its creation
            , authCode="authCodeHashHere"
        )
        newBox.save(force_insert=True)
        return CreateBox(box=newBox)
