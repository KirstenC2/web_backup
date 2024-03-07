###this is app urls

from django.urls import path
from . import views
from .views import register
from .views import get_user_data,register
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views  # Make sure to import auth_views


urlpatterns = [
    path('profile/', views.user_homepage, name='user_homepage'),
    path('', views.main, name='main'),
    path('register/', register, name='register'),
    path('api/profile/<int:user_id>/', get_user_data, name='get_user_data'),
    path('login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('get_all_user_data/', views.get_all_user_data, name='get_all_user_data'),
     path('user/<str:user_id>/', views.get_logged_in_user, name='get_logged_in_user'),
]
