from django.urls import path
from . import views
from .views import CustomSignupView, CustomLoginView

urlpatterns = [
    # Vistas personalizadas desde views.py
    path('', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    
    # Vistas personalizadas que sobrescriben allauth
    path('signup/', CustomSignupView.as_view(), name='account_signup'),
    path('login/', CustomLoginView.as_view(), name='account_login'),
    
    # Vistas predeterminadas de django-allauth que no están personalizadas
    # pero que son necesarias para la funcionalidad completa
    path('logout/', views.LogoutView.as_view(), name='account_logout'),
    path('password/reset/', views.PasswordResetView.as_view(), name='account_reset_password'),
    path('password/change/', views.PasswordResetView.as_view(), name='account_change_password'),
    path('password/reset/done/', views.PasswordResetView.as_view(), name='account_reset_password_done'),
    path('password/reset/key/<uidb36>-<key>/', views.PasswordResetView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/key/done/', views.PasswordResetView.as_view(), name='account_reset_password_from_key_done'),
    path('email/', views.PasswordResetView.as_view(), name='account_email'),
    path('confirm-email/', views.PasswordResetView.as_view(), name='account_email_verification_sent'),
    path('confirm-email/<str:key>/', views.PasswordResetView.as_view(), name='account_confirm_email'),
]


'''
Notas importantes 

Los nombres de las URLs (name=) son importantes y deben mantenerse así porque django-allauth los usa internamente
Algunas vistas como LogoutView y PasswordResetView vienen directamente de allauth pero están importadas en tu views.py
Las rutas de gestión de contraseña y email son necesarias para la funcionalidad completa de autenticación


CREALOS ACA!!!
templates/                      !!!!!!!!!!!!!!!
└── accounts/
    ├── dashboard.html          # Para la vista del panel de usuario
    ├── my_orders.html         # Para la vista de órdenes del usuario
    ├── edit_profile.html      # Para la edición del perfil
    ├── register.html          # Para CustomSignupView (signup)
    ├── login.html             # Para CustomLoginView (login)
    ├── logout.html            # Template para la vista de logout
    ├── password_reset.html    # Formulario inicial de reset de contraseña
    ├── password_reset_done.html      # Confirmación de envío de email
    ├── password_reset_from_key.html  # Formulario para nueva contraseña
    ├── password_reset_from_key_done.html  # Confirmación de cambio
    ├── password_change.html          # Formulario de cambio de contraseña
    ├── email.html                    # Gestión de emails
    ├── email_confirm.html           # Confirmación de email
    └── verification_sent.html       # Aviso de verificación enviada


Te explico cada TEMPLATES DE ACCOUNTS y sus propósitos:

Templates para tus vistas personalizadas:

dashboard.html: Panel principal del usuario
my_orders.html: Lista de órdenes del usuario
edit_profile.html: Formulario de edición de perfil
register.html: Tu formulario personalizado de registro
login.html: Tu formulario personalizado de login


Templates para las vistas de allauth (los nombres necesarios para que funcione correctamente): !!!!!!!!!!!!!!

logout.html: Página de confirmación de cierre de sesión
password_reset.html: Formulario para solicitar reset de contraseña
password_reset_done.html: Confirmación de envío de email
password_reset_from_key.html: Donde el usuario establece nueva contraseña
password_reset_from_key_done.html: Confirmación de cambio exitoso
password_change.html: Formulario para cambiar contraseña
email.html: Gestión de direcciones de email
email_confirm.html: Página de confirmación de email
verification_sent.html: Aviso de email de verificación enviado



Notas importantes:                                  !!!!!!!!

Según tu settings.py, tienes configurado:

ACCOUNT_EMAIL_VERIFICATION = 'mandatory': Por eso son necesarios los templates de verificación de email
ACCOUNT_EMAIL_REQUIRED = True: Los templates relacionados con email son obligatorios
ACCOUNT_USERNAME_REQUIRED = False: Los formularios deberían usar email como identificador principal

También veo que tienes configurado GitHub como proveedor social, así que podrías agregar botones de login social en login.html y register.html
Todos estos templates pueden heredar de un template base para mantener la consistencia en el diseño.

'''