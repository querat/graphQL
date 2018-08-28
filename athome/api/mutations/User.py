import graphene
from graphene_django import DjangoObjectType
from athome.api.models.User import User


class UserNode(DjangoObjectType):
    def resolve_id(self, info):
        return self.id

    class Meta:
        model = User


class UserInput(graphene.InputObjectType):
    name = graphene.String()
    email = graphene.String()
    password = graphene.String()


# TODO avoid duplicate usernames
class CreateUser(graphene.Mutation):

    user = graphene.Field(UserNode)

    class Arguments:
        userInput = graphene.Argument(UserInput)

    @staticmethod
    def mutate(root, info, **kwargs):
        userInput = kwargs.get("userInput")
        dbUser = User(
            name=userInput.name
            , password=userInput.password
            , email=userInput.email
        )
        dbUser.save(force_insert=True)
        return CreateUser(user=dbUser)