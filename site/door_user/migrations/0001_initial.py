# Generated by Django 2.2.5 on 2023-06-28 01:39

from django.db import migrations, models
import django.db.models.deletion
import door_user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('user_course', models.CharField(max_length=100)),
                ('institution_code', models.IntegerField()),
                ('authorization', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rfid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid_uid', door_user.models.Uuid(max_length=6, unique=True)),
                ('authorization', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='door_user.User')),
            ],
        ),
        migrations.CreateModel(
            name='PunchCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punch_in_time', models.DateTimeField()),
                ('punch_out_time', models.DateTimeField(blank=True, null=True)),
                ('teste', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='door_user.User')),
            ],
        ),
    ]
