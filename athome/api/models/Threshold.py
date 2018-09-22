from django.db                  import models
from athome.api.models.Module   import Module

# Class used to represent a threshold of an athome module.
class Threshold(models.Model):

    # Unique identifier of the threshold
    id          = models.AutoField(primary_key=True)

    name        = models.TextField()

    default     = models.IntegerField()

    min         = models.IntegerField()

    max         = models.IntegerField()

    current     = models.IntegerField()

    # module for which the threshold is set.
    module = models.ForeignKey(
        Module
        , related_name="thresholds"     # name of the field in graphQL queries
        , on_delete=models.CASCADE      # Delete thresholds on module removal
        , null=True                     # Nullable, module can have no threshold
    )

