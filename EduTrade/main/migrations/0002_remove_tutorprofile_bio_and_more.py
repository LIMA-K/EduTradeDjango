# Generated by Django 5.2.4 on 2025-07-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorprofile',
            name='bio',
        ),
        migrations.AlterField(
            model_name='tutorprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
