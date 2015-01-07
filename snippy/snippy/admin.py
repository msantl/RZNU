from django.contrib import admin
from snippy.models import Snippet
from django.contrib.auth.models import User

# Register your models here.

admin.site.unregister(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'date')

admin.site.register(User, UserAdmin)
admin.site.register(Snippet, SnippetAdmin)
