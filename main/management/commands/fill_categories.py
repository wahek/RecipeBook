from django.core.management.base import BaseCommand
from main.models import Category


class Command(BaseCommand):
    help = 'Fill categories.txt with file.'

    def handle(self, *args, **options):
        with open('static/categories.txt', 'r', encoding='utf-8') as f:
            for line in f:
                Category.objects.create(name=line.strip('\n'))
                self.stdout.write(self.style.SUCCESS(f'Added {line}'))
