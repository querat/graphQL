from django.contrib import admin

# Register your models here.

from django.contrib import admin
# from myproject.myapp.models import Author
from athome.api.models import *

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Module, AuthorAdmin)
