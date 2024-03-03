from django.contrib import admin


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    search_help_text = 'Поиск по названию и описанию'
    fieldsets = [
        ('Развернуть', {
            'fields': ['name', 'description', 'image', 'cooking_time'],
            'classes': ['collapse']
        })
    ]
