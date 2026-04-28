from django.db import models
from django.conf import settings

from apps.users.services.validators import MaxFileSizeValidator


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/", 
        validators=[MaxFileSizeValidator(5)] ,
        null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} Profile"
    