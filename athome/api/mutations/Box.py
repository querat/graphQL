import  graphene
from    graphql            import GraphQLError
from    graphene_django    import DjangoObjectType
from    athome.api.models  import Box, User


from athome.api.models.Box  import Box

class BoxNode(DjangoObjectType):
    class Meta:
        model = Box


class BoxInput(graphene.InputObjectType):
    userId = graphene.ID()

# class CreateBox(graphene.Mutation):
#     class Arguments:
#         boxInput = graphene.Argument(BoxInput)
#
#     box = graphene.Field(BoxNode)
#
#     @staticmethod
#     def mutate(root, info, **kwargs):
#         boxInput = kwargs.get("boxInput")
#         newBox = Box(
#             ownerUserId = Box.objects.get(pk=boxInput.userId)
#         )
#         newBox.save(force_insert=True)
#         return CreateBox(box=newBox)
#

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

        modifiedBox.ownerUserId = newOwner
        modifiedBox.save(force_update=True)

        return AssignBoxToUser(box=modifiedBox)


class CreateBox(graphene.Mutation):
    # class Arguments:
    #     boxInput = graphene.Argument(BoxInput)

    box = graphene.Field(BoxNode)

    @staticmethod
    def mutate(root, info, **kwargs):
        newBox = Box(
            ownerUserId = None              # No user owns the box at its creation
            , authCode="authCodeHashHere"
        )
        newBox.save(force_insert=True)
        return CreateBox(box=newBox)
