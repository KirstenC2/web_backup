from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,AbstractBaseUser
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



class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length = 200,default="Untitled Image")
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user.username}'s Image {self.id}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_method = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Amount: {self.amount}, Customer ID: {self.customer_id}, User ID: {self.user_id}"