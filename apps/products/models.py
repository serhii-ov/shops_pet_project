from django.db import models
from django.utils.text import slugify
from apps.categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(
        max_length=200, 
        db_index=True, 
        unique=True,
        )
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='product_images/%Y/%m/%d', 
        blank=True,
        )
    # ImageField is better than image_url for local storage

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
