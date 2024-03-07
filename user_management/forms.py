# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.CharField(max_length=10)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Use DateField instead of DateInput
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'date_of_birth']  # Include 'date_of_birth' in fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.date_joined = timezone.now() 
        user.date_of_bith = self.cleaned_data['date_of_birth']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)  # Create a profile for the user
            profile.gender = self.cleaned_data['gender']
            
            profile.save()
        return user

