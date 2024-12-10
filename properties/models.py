from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import os
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.

class Property(models.Model):
    PURPOSE_CHOICES = [
        ('rent', 'For Rent'),
        ('sale', 'For Sale'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('not_available', 'Not Available')
    ]

    property_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    location = models.CharField(max_length=450)
    availability = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES)
    contact = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.property_name)
            unique_slug = base_slug
            counter = 1

            while Property.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)


    def __str__(self):
        return self.property_name

    class Meta:
        ordering = ['-updated_at', '-created_at']


def validate_image(value):
    # Check file extension
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('File type not supported. Please upload a .jpg or .png file.')

    # Check file size (max 850 KB)
    max_size = 850 * 1024  # 850 KB
    if value.size > max_size:
        raise ValidationError('File size too large. Maximum size is 850 KB.')

    # Check image dimensions
    try:
        img = Image.open(value)
        width, height = img.size
        
        # Define maximum dimensions (e.g., 1920x1080)
        max_width = 1920
        max_height = 1144
        
        if width > max_width or height > max_height:
            raise ValidationError(f'Image dimensions too large. Maximum allowed dimensions are {max_width}x{max_height} pixels.')
        
    except Exception as e:
        raise ValidationError(f'Error processing image: {str(e)}')



class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/', validators=[validate_image])



