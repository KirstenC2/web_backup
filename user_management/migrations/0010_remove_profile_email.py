# Generated by Django 5.0.2 on 2024-03-06 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0009_remove_profile_date_joined_remove_profile_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]