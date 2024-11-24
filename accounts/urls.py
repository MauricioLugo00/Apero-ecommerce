from django.urls import path
from . import views
from .views import CustomSignupView, CustomLoginView
from allauth.account.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,  
    PasswordChangeView, 
    EmailView, 
    ConfirmEmailView, 
    EmailVerificationSentView
)

urlpatterns = [
    # Vistas personalizadas desde views.py
    path('', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('contact/', views.contact, name='contact'),

    
    # Vistas personalizadas que sobrescriben allauth
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    
    # Vistas de autenticación de correo electrónico
    path('confirm-email/', EmailVerificationSentView.as_view(
        template_name='accounts/email_verification_sent.html'
    ), name='account_email_verification_sent'),
    
    path('confirm-email/<str:key>/', ConfirmEmailView.as_view(
        template_name='accounts/confirm_email.html'
    ), name='account_confirm_email'),
    
    # Otras vistas de allauth
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), 
         name='account_logout'),
    
    path('password/reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ), name='account_reset_password'),
    
    path('password/change/', PasswordChangeView.as_view(
        template_name='accounts/password_change.html'
    ), name='account_change_password'),
    
    path('email/', EmailView.as_view(
        template_name='accounts/email.html'
    ), name='account_email'),

    path('password/reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='account_reset_password_done'),
]
