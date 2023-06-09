# Generated by Django 4.1.5 on 2023-03-31 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='overall_rating',
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]
