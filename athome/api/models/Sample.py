from django.db                  import models
from athome.api.models.Module   import Module

class Sample(models.Model):

    # unique ID of the sample.
    id          = models.AutoField(primary_key=True)

    # The id of the module that gathered the environmental sample
    # relation defined in Module
    # moduleId = xxx

    # The data and metadata  of the samples sent by the module
    payload     = models.TextField()

    # The date & time the sample was harvested at.
    # Formatted as such: "YYYY-MM-DD hh:mm:ss.µs"
    # For example: 2018-01-02 12:56:13.327164
    date        = models.DateTimeField()

    # The
    moduleId    = models.ForeignKey(
        Module
        , related_name="samples"
        , on_delete=models.CASCADE
    )