from django.urls import path, include
from . import views

urlpatterns = [
    # URLs de allauth
    path('', include('allauth.urls')),
    
    # URLs personalizadas
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]