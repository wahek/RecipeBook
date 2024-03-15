from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RecipeIngredientForm

from .models import Recipe, User, Category, Ingredient, RecipeIngredient, TestIng


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    search_help_text = 'Поиск по названию и описанию'
    filter_horizontal = ['ingredients']
    fieldsets = [
        ('Обязательные', {
            'fields': ['name', 'description', 'ingredients', 'instructions']
        }),
        ('Дополнительные', {
            'fields': ['cooking_time', 'author', 'view', 'img', 'is_active'],
            'classes': ['collapse']
        })
    ]


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    add_fieldsets = [
        *UserAdmin.add_fieldsets,
        ('Дополнительно', {
            'fields': ['email', 'gender', 'birth_date'],
        })
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'img']


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    form = RecipeIngredientForm


admin.site.register(Ingredient)
admin.site.register(TestIng)
