from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields here
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(max_length = 50, default = 'example@gmail.com' )

    # Add any other fields you need

    def __str__(self):
        return self.user.username


class UserManagementProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_joined = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'user_management_profile'