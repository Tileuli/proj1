# Generated by Django 4.1.5 on 2023-04-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(),
        ),
    ]
