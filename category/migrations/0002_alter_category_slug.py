# Generated by Django 3.2.8 on 2021-11-01 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=300, unique=True),
        ),
    ]
