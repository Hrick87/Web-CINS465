# Generated by Django 3.2.8 on 2021-12-11 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='comment',
            field=models.CharField(max_length=240, null=True),
        ),
    ]
