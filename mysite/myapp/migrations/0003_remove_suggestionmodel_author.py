# Generated by Django 3.2.8 on 2021-11-17 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_suggestionmodel_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestionmodel',
            name='author',
        ),
    ]
