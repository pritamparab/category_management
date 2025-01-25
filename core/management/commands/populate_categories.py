from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Populate the database with default categories'

    def handle(self, *args, **kwargs):
        categories = [
            "men's clothing",
            "women's clothing",
            "jewelery",
            "electronics",
            "Mobile Phone",
        ]
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Categories populated successfully.'))