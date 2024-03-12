from django.core.management.base import BaseCommand
from main.models import Ingredient


class Command(BaseCommand):
    help = 'Fill ingredients.txt with file.'

    def handle(self, *args, **options):
        with open('static/ingredients.txt', 'r', encoding='utf-8') as f:
            for line in f:
                Ingredient.objects.create(name=line.strip('\n'))
                self.stdout.write(self.style.SUCCESS(f'Added {line}'))
