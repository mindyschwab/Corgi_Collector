# Generated by Django 4.1.7 on 2023-03-30 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_corgi_toys'),
    ]

    operations = [
        migrations.AddField(
            model_name='toy',
            name='description',
            field=models.TextField(default='', max_length=200),
        ),
    ]