# Generated by Django 5.0 on 2023-12-28 05:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_category_options_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(unique=True, validators=[django.core.validators.RegexValidator('[0-9]+')]),
        ),
    ]
