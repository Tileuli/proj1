# Generated by Django 4.1.5 on 2023-05-03 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_item_last_viewed_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='last_viewed_by',
        ),
    ]