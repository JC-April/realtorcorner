# Generated by Django 5.1.3 on 2024-11-30 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_property_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='property',
            options={'ordering': ['-updated_at', '-created_at']},
        ),
    ]
