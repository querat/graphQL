import graphene
from graphql import GraphQLError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from athome.api.models.User import User
import bcrypt
import email

from athome.api.mutations.nodes.User import UserNode


class UserInput(graphene.InputObjectType):

    name = graphene.String()
    email = graphene.String()
    password = graphene.String()

    def validate(self):
        requiredArgs = ["name", "email", "password"]
        for requiredArg in requiredArgs:
            if getattr(self, requiredArg, None) is None:
                return False, f"Missing element in userInput: {requiredArg}"
        if User.objects.filter(name=self.name).first():
            return False, f"Username {self.name} is already taken !"
        if User.objects.filter(email=self.email).first():
            return False, f"email already in use: {self.email}"
        try:
            validate_email(self.email)
        except ValidationError as e:
            return False, f"invalid email: {self.email}"
        return True, "ok"


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        userInput = graphene.Argument(UserInput)

    @staticmethod
    def mutate(root, info, **kwargs):
        userInput = kwargs.get("userInput")

        if userInput is None:
            raise GraphQLError("Missing argument: userInput")

        ok, msg = userInput.validate()
        if not ok:
            raise GraphQLError(msg)

        # Unique salt for each User. is stored in the password hash itself by bcrypt
        hashedPw = bcrypt.hashpw(userInput.password.encode('utf8'), bcrypt.gensalt())
        dbUser = User(
            name=userInput.name
            , password=hashedPw.decode()
            , email=userInput.email
        )
        dbUser.save(force_insert=True)
        return CreateUser(user=dbUser)
