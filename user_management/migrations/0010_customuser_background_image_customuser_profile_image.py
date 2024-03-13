# Generated by Django 5.0.2 on 2024-03-13 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0009_usermanagementprofile_customuser_alter_profile_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='background_images/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
