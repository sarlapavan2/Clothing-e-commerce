from django.db import models
import uuid
from django.utils.text import slugify 

def product_image_path(instance, filename):
    ext = filename.split('.')[-1]           # jpg / png / webp
    new_filename = f"{uuid.uuid4()}.{ext}"  # unique name

    if instance.gender == 'M':
        return f'photos/categories/men/{new_filename}'
    return f'photos/categories/women/{new_filename}'



class Product(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    PRODUCT_TYPE_CHOICES = (
        ('HOODIE', 'Hoodie'),
        ('JACKET', 'Jacket'),
        ('SHIRT', 'Shirt'),
        ('PANT', 'Pant'),
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    # image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='HOODIE')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
