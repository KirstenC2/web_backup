from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.AutoField(primary_key=True,default= 1000) 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields as needed
