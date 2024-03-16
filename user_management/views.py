import datetime
from django.shortcuts import render, redirect,get_object_or_404
from django.template import loader
from django.http import HttpResponse,JsonResponse
from .models import *
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
from django.shortcuts import render, redirect
from .forms import ImageForm

from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY
BASE_DOMAIN = settings.BASE_DOMAIN


from django.shortcuts import redirect
from django.conf import settings
#Google login


def google_oauth_callback(request):
    code = request.GET.get('code')
    redirect_uri = 'http://localhost:8000/accounts/google/login/callback/'  # Replace with your redirect URI
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET

    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=token_data)
    token = response.json().get('access_token')

    if token:
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        # Authenticate and login the user
        user = authenticate(request, google_id=user_info['sub'])
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
    return redirect('login')  # Redirect to login page if authentication fails

def google_oauth_redirect(request):
    redirect_uri = 'http://localhost:8000/accounts/google/login/callback/'  # Replace with your redirect URI
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    scope = 'openid email profile'
    auth_url = f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
    return redirect(auth_url)

def google_oauth_callback(request):
    code = request.GET.get('code')
    redirect_uri = 'http://localhost:8000/accounts/google/login/callback/'  # Replace with your redirect URI
    client_id = settings.GOOGLE_OAUTH2_CLIENT_ID
    client_secret = settings.GOOGLE_OAUTH2_CLIENT_SECRET

    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=token_data)
    token = response.json().get('access_token')

    if token:
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()


def user_homepage(request):
    return render(request, 'user_management/profile.html')

def priceplan(request):

    return render(request, 'user_management/priceplan.html')





def profile(request):
    # Retrieve all images uploaded by the current user
    user_images = Image.objects.filter(user=request.user)

    return render(request, 'profile.html', {'user_images': user_images})


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



#@login_required
def get_logged_in_user(request):
    user = request.user
    if user.is_authenticated:
        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            
        }
        return JsonResponse({'user_data': user_data})
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

def set_cookie_view(request):
    response = HttpResponse("Setting a cookie!")
    response.set_cookie("my_cookie", "my_value", max_age=3600)  # Set a cookie named "my_cookie" with a value and a maximum age of 1 hour (in seconds)
    return response
 

from django.http import JsonResponse
from django.core.serializers import serialize
def show_user_images(request):
    # Fetch all images associated with the currently logged-in user
    user_images = Image.objects.filter(user_id=request.user.id)
    
    # Serialize the queryset to JSON
    user_images_json = serialize('json', user_images)
    
    # Return the JSON response
    return JsonResponse(user_images_json, safe=False)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)

            # Render the user homepage with user and user_images
            return render(request, 'user_homepage.html', {'user': user, 'user_images': user_images})
        else:
            # Handle invalid login credentials
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

# Define the redirect URI for Google OAuth2
redirect_uri = 'http://localhost:8000/accounts/google/login/callback/'

# Google OAuth2 login view
def google_login(request):
    if 'id_token' in request.POST:
        try:
            idinfo = id_token.verify_oauth2_token(request.POST['id_token'], requests.Request(), settings.SOCIALACCOUNT_GOOGLE_CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            user = authenticate(request, google_id=idinfo['sub'])
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
        except ValueError:
            pass
    return redirect('login')  # Redirect to login page if authentication fails


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout



def get_logged_in_user_data(request):
    user = request.user
    if user.is_authenticated:
        user_data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            # Add any additional fields you want to retrieve here
        }
        return JsonResponse({'user_data': user_data})
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)
    



def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)
            image_instance.user = request.user
            image_instance.save()
            return redirect('user_homepage')
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})


















endpoint_secret = 'whsec_066d2c4526ad54fdf6c36e2b3891810e0a8d72990c06c8347464f6f446f19c34'



@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'success': False}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'success': False}, status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        payment_id = session['id']
        amount = session['amount_total'] / 100  # Convert from cents to dollars
        currency = session['currency'].upper()
        payment_method = session['payment_method_types'][0]
        customer_id = session['customer']
        
        # Get or create the user associated with the customer ID
        user = None  # You need to implement this part according to your user model and Stripe Customer objects

        # Create Payment instance and save to database
        payment = Payment.objects.create(
            user=user,
            payment_id=payment_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            customer_id=customer_id,
        )

        return JsonResponse({'success': True})  # Respond with success
    else:
        # Unexpected event type
        return JsonResponse({'success': False})