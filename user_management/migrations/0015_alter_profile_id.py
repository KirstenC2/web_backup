# Generated by Django 5.0.2 on 2024-03-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0014_remove_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]