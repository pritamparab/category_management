from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Populate the database with default categories'

    def handle(self, *args, **kwargs):
        categories = [
            "Men's Clothing",
            "Women's Clothing",
            "Jewellery",
            "Electronics",
            "Mobile Phones",
        ]
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Categories populated successfully.'))