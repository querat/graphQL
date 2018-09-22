from django.db import models
from athome.api.models.User import User

# Class used to represent a central AtHome box
class Box(models.Model):

    # Unique identifier of the box
    id          = models.AutoField(primary_key=True)

    # Code the box needs to send to authenticate
    authCode    = models.TextField()

    # User owning the box
    user = models.ForeignKey(
        User
        , related_name="boxes"          # name of the field in graphQL queries
        , on_delete=models.DO_NOTHING   # Box still exists on user deletion
        , null=True                     # Nullable, box can have no user assigned
    )

