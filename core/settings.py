import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps locales
    'accounts',
    'carts',
    'categories',
    'orders',
    'store',

    # django-allauth
    'django.contrib.sites',  # Requerido por allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',

    # Otras
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ruta de las plantillas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('DB_NAME'),
#        'USER': os.getenv('DB_USER'),
#        'PASSWORD': os.getenv('DB_PASSWORD'),
#        'HOST': os.getenv('DB_HOST', 'localhost'),
#        'PORT': os.getenv('DB_PORT', '5432'),
#    }
#}

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL')) 
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de idiomas y zonas horarias
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# Configuración de usuario personalizado
AUTH_USER_MODEL = 'accounts.Account'

# CONFIGURACION DE DJANGO-ALLAUTH

SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend predeterminado de Django
    'allauth.account.auth_backends.AuthenticationBackend',  # Backend de allauth
]
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_URL = 'account_login'  # Vista predeterminada de inicio de sesión de allauth
LOGIN_REDIRECT_URL = 'home'  # URL de redirección después de iniciar sesión
# URL de redirección después de cerrar sesión
LOGOUT_REDIRECT_URL = 'account_login'
ACCOUNT_LOGOUT_ON_GET = True  # Cierra sesión al acceder a la URL de logout


SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': os.getenv('GITHUB_CLIENT_ID'),
            'secret': os.getenv('GITHUB_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'user',
            'email',
        ],
        'AUTH_PARAMS': {
            'redirect_uri': 'http://localhost:8000/accounts/github/login/callback/'
        }
    }
}


# Configuración de correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')  # Servidor de correo
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)  # Puerto SMTP
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'  # Seguridad
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Email del remitente
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Contraseña del email
# Correo predeterminado para enviar mensajes
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# PayPal Sandbox credentials
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID_SANDBOX')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET_SANDBOX')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
