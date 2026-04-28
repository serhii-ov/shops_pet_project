from django.db.models.signals import (
    post_migrate,
    )
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group, 
    Permission,
    )


User = get_user_model()
GROUPS = ["Admin", "Staff", "Customer"]


@receiver(post_migrate)
def setup_roles(sender, **kwargs):
    groups = {}

    for name in GROUPS:
        group, _ = Group.objects.get_or_create(name=name)
        groups[name] = group

    # Assign permissions
    groups["Admin"].permissions.set(Permission.objects.all())

    groups["Staff"].permissions.set(
        Permission.objects.filter(codename__in=[
            "view_user",
            "change_user",
        ])
    )

    groups["Customer"].permissions.set(
        Permission.objects.filter(codename="view_user")
    )


# @receiver(post_save, sender=User)
# from .models import Profile
# def create_profile(sender, instance, created, **kwargs):
#     if created and hasattr(instance, "email"):
#         Profile.objects.get_or_create(user=instance)
