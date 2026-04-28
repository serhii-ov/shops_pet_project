from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.db import transaction


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)

        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            # assign default group
            if not extra_fields.get("is_superuser"):
                group, _ = Group.objects.get_or_create(name="Customer")
                if group:
                    user.groups.add(group)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        user = self.create_user(email, password, **extra_fields)

        admin_group = Group.objects.get(name="Admin")
        user.groups.add(admin_group)

        return user
