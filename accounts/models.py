from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin

# Clase para definir tipos de usuarios
class MyAccountManager(BaseUserManager):
    
    '''
    Esta función _crear_usuario se encarga de la lógica común para crear un usuario en la base de datos, ya sea un usuario normal o un superusuario.
    '''
    def _create_user(self, first_name, last_name, username, email, password=None, **extra_fields): 
        # Verifica que el usuario tenga un email
        if not email:
            raise ValueError('El usuario debe tener un email') 
        # Verifica que el usuario tenga un nombre de usuario
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        
        # Normaliza el email
        email = self.normalize_email(email) 
        
        # Crea la instancia del usuario
        user = self.model(
            email=email,                                # Asigna el email normalizado
            username= username,                         # Asigna el nombre de usuario
            first_name=first_name,                      # Asigna nombre
            last_name=last_name,                        # Asigna apellido
        )
        
        # Asigna contraseña al usuario y verifica que se haya digitado una contraseña
        if password:
            user.set_password(password)  # Establece la contraseña encriptada
        else:
            raise ValueError('El usuario debe tener una contraseña') 
        
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
        """Crea y guarda un usuario normal con el email y la contraseña dados."""
        extra_fields.setdefault('is_staff', False)  # Niega permisos de staff a clientes
        extra_fields.setdefault('is_superuser', False)  # Niega que sea un superusuario
        return self._create_user(first_name, last_name, username, email, password, **extra_fields)
    
    def create_superuser(self, first_name, last_name, username, email, password=None, **extra_fields):
        """Crea y guarda un superusuario con el email y la contraseña dados."""
        extra_fields.setdefault('is_staff', True)  # Proporciona permisos de staff a superusuarios
        extra_fields.setdefault('is_superuser', True)  # Permite que se identifique como un superusuario
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe ser identificado como superuser.')
        
        return self._create_user(first_name, last_name, username, email, password, **extra_fields)
    
# Clase para definir usuarios
class Accounts(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=150, unique=True, 
                                help_text='Requerido: Ingresa un nombre de usuario.',
                                error_messages= {
                                    'Unico': 'Nombre de usuario no disponble! Intente con otro por favor.'
                                    }
                                )
    first_name = models.CharField(("first_name"), max_length=50, blank=True)
    last_name = models.CharField(("last_name"), max_length=50, blank=True)
    email = models.EmailField(("email"), unique=True)
    start_date = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Atributos
    is_admin = models.BooleanField(default=False)  
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Para gestionar si el usuario está activo o inactivo
    is_superadmin = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='cuentas_user_set',  # Cambiar related_name
        blank=True,
        help_text='Los grupos a los que pertenece el usuario.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='cuentas_user_set',  # Cambiar related_name
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='user permissions',
    )
    
    objects = MyAccountManager()
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'username', 'first_name', 'last_name'] #Filas requeridas para crear un usuario
   
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    
    def full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
    
    def user_email(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

PAISES_LATINOAMERICANOS = [
    ('AR', 'Argentina'),
    ('BO', 'Bolivia'),
    ('BR', 'Brasil'),
    ('CL', 'Chile'),
    ('CO', 'Colombia'),
    ('CR', 'Costa Rica'),
    ('CU', 'Cuba'),
    ('DO', 'República Dominicana'),
    ('EC', 'Ecuador'),
    ('SV', 'El Salvador'),
    ('GT', 'Guatemala'),
    ('HN', 'Honduras'),
    ('MX', 'México'),
    ('NI', 'Nicaragua'),
    ('PA', 'Panamá'),
    ('PY', 'Paraguay'),
    ('PE', 'Perú'),
    ('UY', 'Uruguay'),
    ('VE', 'Venezuela'),
]
    
DEPARTAMENTOS_LATINOAMERICA = [
    ('AR_BUE', 'Buenos Aires, Argentina'),
    ('BO_LPZ', 'La Paz, Bolivia'),
    ('BR_SPA', 'São Paulo, Brasil'),
    ('CL_STG', 'Santiago, Chile'),
    ('CO_ANT', 'Antioquia, Colombia'),
    ('CO_ATL', 'Atlántico, Colombia'),
    ('CO_BOL', 'Bolívar, Colombia'),
    ('CO_BOG', 'Cundinamarca, Colombia'),
    ('CO_MAG', 'Magdalena, Colombia'),
    ('CO_VAL', 'Valle del Cauca, Colombia'),
    ('CR_SJO', 'San José, Costa Rica'),
    ('CU_HAV', 'La Habana, Cuba'),
    ('DO_SDO', 'Santo Domingo, República Dominicana'),
    ('EC_PCH', 'Pichincha, Ecuador'),
    ('SV_SAL', 'San Salvador, El Salvador'),
    ('GT_GUA', 'Guatemala, Guatemala'),
    ('HN_FMZ', 'Francisco Morazán, Honduras'),
    ('MX_CMX', 'Ciudad de México, México'),
    ('NI_MNG', 'Managua, Nicaragua'),
    ('PA_PAC', 'Panamá, Panamá'),
    ('PY_ASU', 'Asunción, Paraguay'),
    ('PE_LIM', 'Lima, Perú'),
    ('UY_MVD', 'Montevideo, Uruguay'),
    ('VE_CCS', 'Caracas, Venezuela'),
]
    
CIUDADES_LATINOAMERICA = [
    ('AR_BUE', 'Buenos Aires'),
    ('BO_LPZ', 'La Paz'),
    ('BR_SPA', 'São Paulo'),
    ('CL_STG', 'Santiago'),
    ('CO_ANT', 'Medellín'),
    ('CO_ATL', 'Barranquilla'),
    ('CO_BOL', 'Cartagena de Indias'),
    ('CO_BOG', 'Bogotá'),
    ('CO_MAG', 'Santa Marta'),
    ('CO_VAL', 'Cali'),
    ('CR_SJO', 'San José'),
    ('CU_HAV', 'La Habana'),
    ('DO_SDO', 'Santo Domingo'),
    ('EC_PCH', 'Quito'),
    ('SV_SAL', 'San Salvador'),
    ('GT_GUA', 'Guatemala'),
    ('HN_FMZ', 'Tegucigalpa'),
    ('MX_CMX', 'Ciudad de México'),
    ('NI_MNG', 'Managua'),
    ('PA_PAC', 'Ciudad de Panamá'),
    ('PY_ASU', 'Asunción'),
    ('PE_LIM', 'Lima'),
    ('UY_MVD', 'Montevideo'),
    ('VE_CCS', 'Caracas'),
]

# Clase para crear un perfil de usuario                
class UserProfile(models.Model):
    user = models.OneToOneField(Accounts, on_delete=models.CASCADE)             # Un perfil por cada cuenta de usuario
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    country = models.CharField(max_length=2, choices=PAISES_LATINOAMERICANOS, default='CO')
    state = models.CharField(max_length=20, choices=DEPARTAMENTOS_LATINOAMERICA, blank=False)
    city = models.CharField(max_length=50, choices=CIUDADES_LATINOAMERICA, blank=False)
    
    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'


