# Generated by Django 2.2.5 on 2023-07-09 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('door_user', '0002_auto_20230708_1458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='punchcard',
            name='teste',
        ),
        migrations.AddField(
            model_name='punchcard',
            name='out',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='punchcard',
            name='reviw',
            field=models.BooleanField(default=False),
        ),
    ]
