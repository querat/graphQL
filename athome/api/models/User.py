from django.db import models

class User(models.Model):

    # Unique identifier
    id = models.AutoField(primary_key=True)

    # Nickname choosen by the user
    name = models.TextField(unique=True)

    # Password of the user. Hashed and salted
    password = models.TextField()

    # Email of the user
    email = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.name