from django.contrib             import admin
from athome.api.models.Box      import Box
from athome.api.models.User     import User
from athome.api.models.Sample   import Sample
from athome.api.models.Module   import Module

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, AuthorAdmin)
admin.site.register(Box, AuthorAdmin)
admin.site.register(Module, AuthorAdmin)
admin.site.register(Sample, AuthorAdmin)
