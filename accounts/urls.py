from django.urls import path
from . import views
from .views import CustomSignupView, CustomLoginView
from allauth.account.views import LogoutView, PasswordResetView, PasswordChangeView, EmailView, ConfirmEmailView

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
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('password/change/', PasswordChangeView.as_view(), name='account_change_password'),
    path('password/reset/done/', PasswordResetView.as_view(), name='account_reset_password_done'),
    path('password/reset/key/<uidb36>-<key>/', PasswordResetView.as_view(), name='account_reset_password_from_key'),
    path('password/reset/key/done/', PasswordResetView.as_view(), name='account_reset_password_from_key_done'),
    path('email/', EmailView.as_view(), name='account_email'),
    path('confirm-email/', ConfirmEmailView.as_view(), name='account_email_verification_sent'),
    path('confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
]


'''
Notas importantes 

Vistas personalizadas en views.py:

dashboard.html: Panel principal del usuario.
my_orders.html: Lista de órdenes del usuario.
edit_profile.html: Formulario para editar el perfil del usuario.



Vistas personalizadas de allauth (sobrescritas):

signup.html: Formulario de registro personalizado (CustomSignupView).
login.html: Formulario de inicio de sesión personalizado (CustomLoginView).


Vistas predeterminadas de allauth (necesarias para la funcionalidad completa):

Autenticación y recuperación de contraseñas:
logout.html: Confirmación de cierre de sesión.
password_reset.html: Formulario para solicitar el restablecimiento de contraseña.
password_reset_done.html: Confirmación de envío de email para reset.
password_reset_from_key.html: Formulario para establecer nueva contraseña.
password_reset_from_key_done.html: Confirmación de cambio de contraseña.
password_change.html: Formulario para cambiar la contraseña.
Gestión de emails:
email.html: Gestión de direcciones de email del usuario.
email_confirm.html: Página de confirmación de email.
verification_sent.html: Aviso de verificación de email enviado.

Notas importantes:

Los nombres de las URLs son esenciales para que django-allauth funcione correctamente.
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' y ACCOUNT_EMAIL_REQUIRED = True requieren plantillas de verificación y gestión de emails.
ACCOUNT_USERNAME_REQUIRED = False significa que se utiliza el email como identificador, no el nombre de usuario.
Si usas GitHub como proveedor social, considera agregar botones de login social en login.html y register.html.
Todos los templates pueden heredar de una plantilla base común para mantener la consistencia en el diseño.

'''