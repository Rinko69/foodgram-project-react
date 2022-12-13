from django.contrib import admin

from .models import Ingredient, Recipe, Tag
from users.models import Follow, MyUser

admin.site.register(MyUser)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe)

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'password',
        'role',
    )
    search_fields = ('first_name', 'last_name', 'email')

admin.site.register(Follow)