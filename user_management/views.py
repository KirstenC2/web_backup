import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.template import loader
from django.http import HttpResponse,JsonResponse
from .models import Profile
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.shortcuts import render, redirect
import uuid
from django.urls import reverse
import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CustomUserCreationForm
import random
from django.http import HttpResponse, HttpResponseRedirect


stripe.api_key = settings.STRIPE_SECRET_KEY

def user_homepage(request):
    return render(request, 'user_management/profile.html')





def main(request):
  return render(request, 'main.html')


def get_user_data(request, user_id):
    # Retrieve the User object based on the user_id
    user = get_object_or_404(User, id=user_id)

    # Prepare the user data as a dictionary
    user_data = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        # Add other fields from the User model as needed
    }
    
    # Return user data as JSON response
    return JsonResponse(user_data)





def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_management/register.html', {'form': form})


def create_payment(request):
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                description='Example charge'
            )
            return JsonResponse({'success': True})
        except stripe.error.CardError as e:
            # Handle card errors
            return JsonResponse({'error': str(e)})
        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            return JsonResponse({'error': str(e)})
        


def get_all_user_data(request):
    # Retrieve all User objects
    users = User.objects.all()
    
    # Prepare user data as a list of dictionaries
    user_data = []
    for user in users:
        user_info = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            # Add other fields from the User model as needed
        }
        user_data.append(user_info)
    
    # Return user data as JSON response
    return JsonResponse(user_data, safe=False)



@login_required
def get_logged_in_user(request, user_id):
    # Check if the requested user ID matches the logged-in user's ID
    if str(request.user.id) != user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    # Retrieve the user object from the database
    user = get_object_or_404(User, id=user_id)

    # Prepare user data
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        # Add other fields as needed
    }

    # Return user data as JSON response
    return JsonResponse(user_data)

def setting_cookie(request, username):
    response = HttpResponse()
    response.set_cookie('Username', username)

    return 0



def getting_cookie(request):
    usernameCookie = request.COOKIES.get('Username', '')
    return usernameCookie


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if setting_cookie(request,username)==0:
                login(request, user)
                return render(request, 'user_homepage.html')
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
def user_profile(request):
    # Retrieve session data
    username = request.COOKIES.get('username')

    # Print session data to console
    print("Session username:", username)

    # Add your other view logic here

    return render(request, 'user_management/profile.html', {'username': username})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout