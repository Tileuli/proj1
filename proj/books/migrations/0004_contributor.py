# Generated by Django 4.1.5 on 2023-04-01 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_book_overall_rating_review_rating_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_names', models.CharField(max_length=50)),
                ('last_names', models.CharField(max_length=50)),
            ],
        ),
    ]
