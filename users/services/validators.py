from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, max_size_mb):
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        if value.size > self.max_size_mb * 1024 * 1024:
            raise ValidationError(f"File cannot exceed {self.max_size_mb}MB.")
