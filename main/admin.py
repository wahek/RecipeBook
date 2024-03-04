from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Recipe, User
from .forms import UserCreationForm, UserChangeForm


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    search_help_text = 'Поиск по названию и описанию'
    fieldsets = [
        ('Развернуть', {
            'fields': ['name', 'description', 'image', 'cooking_time'],
            'classes': ['collapse']
        })
    ]


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    add_fieldsets = [
        *UserAdmin.add_fieldsets,
        ('Дополнительно', {
            'fields': ['email', 'age', 'gender']
        })
    ]

