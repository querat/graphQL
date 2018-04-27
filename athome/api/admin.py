from django.contrib     import admin
from athome.api.models  import *

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Module, AuthorAdmin)
admin.site.register(Sample, AuthorAdmin)