import os
import sys
import django

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from core.models import Category

def setup_groups():
    categories = Category.objects.all()

    # Define groups
    groups_data = {
        'Group A': ["men's clothing", "women's clothing"],
        'Group B': ["men's clothing", "jewelery"],
        'Group C': ["jewelery", "electronics"],
    }

    #Premium group
    premium_group, created = Group.objects.get_or_create(name='Premium')

    mobile_phones_permission, _ = Permission.objects.get_or_create(
        codename="access_mobile_phone",
        name="Can access Mobile Phone",
        content_type=ContentType.objects.get_for_model(Category),
    )
    premium_group.permissions.add(mobile_phones_permission)

    for group_name, category_names in groups_data.items():
        group, created = Group.objects.get_or_create(name=group_name)

        # Assign permissions to the group
        for category_name in category_names:
            category = categories.filter(name=category_name).first()
            if category:
                content_type = ContentType.objects.get_for_model(Category)

                # Create permission
                permission, _ = Permission.objects.get_or_create(
                    codename=f'access_{category.name.replace(" ", "_")}',
                    name=f'Can access {category.name}',
                    content_type=content_type,
                )
                group.permissions.add(permission)

    print("Groups and permissions setup completed.")

if __name__ == "__main__":
    setup_groups()
