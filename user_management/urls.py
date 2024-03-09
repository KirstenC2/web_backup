###this is app urls

from django.urls import path
from . import views
from .views import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views  # Make sure to import auth_views


urlpatterns = [
    path('profile/', views.user_homepage, name='user_homepage'),
    path('', views.main, name='main'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('accounts/profile/', views.user_homepage, name='user_homepage'),
    path('get_all_user_data/', views.get_all_user_data, name='get_all_user_data'),
    path('user/<str:user_id>/', views.get_logged_in_user, name='get_logged_in_user'),
    path('setc/<str:username>/', views.setting_cookie, name='setc'),
    path('getc/', views.getting_cookie, name='getc')
]
