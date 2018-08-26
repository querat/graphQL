from django.db import models
from athome.api.models.Box import Box

class Module(models.Model):

    # The unique identifier of the module
    id          = models.AutoField(primary_key=True)

    # Mac address of the module
    # Under the format xx:xx:xx:xx:xx:xx
    # Where x represent an hexadecimal digit
    mac         = models.TextField()

    # The name of the module
    # Either the default one or
    # one choosen by the user
    name        = models.TextField()

    # The room where the module is located
    location    = models.TextField()

    # The type of module, returned as a lower case String
    # As of now, can be either:
    # - hygrometer
    # - thermometer
    # - luxmeter
    # - athmospherics
    type        = models.TextField()

    # The vendor of the module
    # "athome"
    vendor      = models.TextField()

    # environmental samples gathered by the module.
    # (see the Sample type)
    # returned as an array
    # samples = # (See models/Sample.py

    box         = models.ForeignKey(
        Box
        , null=True
        , related_name="modules"
        , on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name
