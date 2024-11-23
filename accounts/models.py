from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Administrador personalizado para la creación de usuarios
class MyAccountManager(BaseUserManager):
    # Método para crear un usuario estándar
    def create_user(self, first_name, last_name, username, email, password=None):
        # Validación de que el usuario tenga un correo electrónico
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        # Validación de que el usuario tenga un nombre de usuario
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        
        # Normaliza el correo electrónico y crea el usuario
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        
        # Establece la contraseña y guarda el usuario
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Método para crear un superusuario
    def create_superuser(self, first_name, last_name, username, email, password):
        # Utiliza el método de creación de usuario para crear un superusuario
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        # Asigna permisos de administrador al superusuario
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

# Modelo de cuenta personalizado que extiende AbstractBaseUser y PermissionsMixin
class Account(AbstractBaseUser, PermissionsMixin):
    # Opciones de roles para el usuario
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('customer', 'Cliente'),
        ('seller', 'Vendedor'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    # Validador para el formato del número de teléfono
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    # Campos de estado y permisos
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    # Configuración del modelo de usuario personalizado
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # Especifica el administrador personalizado para este modelo
    objects = MyAccountManager()

    # Cadena de texto que representa al objeto
    def __str__(self):
        return self.email

    # Métodos para verificar permisos
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# Modelo para perfil de usuario extendido
class UserProfile(models.Model):
    # Relación uno a uno con el modelo de cuenta
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='static/images/user_profile/', blank=True, null=True)

    # Cadena de texto que representa al objeto
    def __str__(self):
        return self.user.first_name

    # Método para obtener la dirección completa del perfil
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
