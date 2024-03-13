from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views  # Make sure to import auth_views
from .views import google_oauth_redirect, google_login

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
    path('accounts/google/login/callback/', views.google_oauth_redirect, name='google_oauth_callback'),  
    path('auth/google/', google_login, name='google_login'),  # Google OAuth login view
    #path('accounts/google/login/callback/', google_oauth_callback, name='google_oauth_callback'),  # Google OAuth callback view

    path('process_payment/', views.process_payment, name='process_payment'),
    path('create_subscription/', views.create_subscription, name='create_subscription'),
    path('handle_webhook/', views.handle_webhook, name='handle_webhook'),
    path('generate_report/', views.generate_report, name='generate_report'),


]
