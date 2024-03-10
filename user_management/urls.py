###this is app urls

from django.urls import path,include
from . import views
from .views import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views  # Make sure to import auth_views


urlpatterns = [
    path('profile/', views.user_homepage, name='user_homepage'),
    path('', views.main, name='main'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('accounts/profile/', views.user_homepage, name='user_homepage'),
    path('get_all_user_data/', views.get_all_user_data, name='get_all_user_data'),
    path('user/<str:user_id>/', views.get_logged_in_user, name='get_logged_in_user'),
    path('setc/', views.show_user_images, name='setc'),
    path('accounts/', include('allauth.urls')),
    path('accounts/google/login/', views.google_oauth_redirect, name='google_oauth_redirect'),  # Google OAuth redirect view
    path('accounts/google/login/callback/', views.google_oauth_callback, name='google_oauth_callback'),  # Google OAuth callback view
]