from django.db import models
from athome.api.models.User import User


# Class used to represent a central AtHome box
class Solution(models.Model):
    # Unique identifier of the box
    id = models.AutoField(primary_key=True)

    # Code the box needs to send to authenticate
    authCode = models.TextField()
