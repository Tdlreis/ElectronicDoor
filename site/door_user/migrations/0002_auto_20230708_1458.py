# Generated by Django 2.2.5 on 2023-07-08 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('door_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfid',
            name='rfid_uid',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
