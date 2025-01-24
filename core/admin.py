from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from core.models import Category

# Action to make users premium
def make_premium(modeladmin, request, queryset):
    premium_group, created = Group.objects.get_or_create(name='Premium')
    for user in queryset:
        user.groups.add(premium_group)
        # Add the "Mobile Phones" permission
        mobile_phones_permission, _ = Permission.objects.get_or_create(
            codename="access_mobile_phones",
            name="Can access Mobile Phones",
            content_type=ContentType.objects.get_for_model(Category),
        )
        user.user_permissions.add(mobile_phones_permission)

make_premium.short_description = "Make selected users premium"

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('premium_status',)

    def premium_status(self, obj):
        return obj.groups.filter(name='Premium').exists()

    premium_status.boolean = True
    premium_status.short_description = 'Premium Member'

    def save_model(self, request, obj, form, change):
        # Get the Premium group
        premium_group, _ = Group.objects.get_or_create(name='Premium')

        # Get the user's current groups from the form data
        selected_groups = form.cleaned_data.get('groups', obj.groups.all())
        is_premium_selected = premium_group in selected_groups

        # Ensure the user belongs to at least one non-premium group if Premium is selected
        normal_groups = [group for group in selected_groups if group.name != 'Premium']
        if is_premium_selected and not normal_groups:
            raise ValidationError(
                "A user cannot be added to the Premium group without belonging to at least one other group."
            )

        # Call the parent class's save_model to save the user first
        super().save_model(request, obj, form, change)

        # Handle permissions based on group membership
        if premium_group in obj.groups.all():
            # Add the Mobile Phones permission
            mobile_phones_permission, _ = Permission.objects.get_or_create(
                codename="access_mobile_phones",
                name="Can access Mobile Phones",
                content_type=ContentType.objects.get_for_model(Category),
            )
            obj.user_permissions.add(mobile_phones_permission)
        else:
            # Remove the Mobile Phones permission if Premium is removed
            mobile_phones_permission = Permission.objects.filter(codename="access_mobile_phones").first()
            if mobile_phones_permission:
                obj.user_permissions.remove(mobile_phones_permission)

        # Remove Premium group if the user is not in any other group
        if not obj.groups.exclude(name='Premium').exists() and premium_group in obj.groups.all():
            obj.groups.remove(premium_group)

        obj.save()

# Unregister the default UserAdmin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)