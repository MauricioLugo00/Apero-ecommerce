from django import forms
from .models import Account, UserProfile
from allauth.account.forms import SignupForm
from .models import ContactMessage

# Formulario de registro personalizado que extiende SignupForm de django-allauth
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, label='Nombre')
    last_name = forms.CharField(max_length=50, label='Apellido')
    phone_number = forms.CharField(max_length=15, label='Número de teléfono', required=False)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        
        # Crear perfil de usuario asociado si no existe
        UserProfile.objects.get_or_create(user=user)
        
        return user


# Formulario para editar la información básica del usuario
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clase CSS a cada campo del formulario
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

# Formulario para editar el perfil del usuario
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False, 
        error_messages={'invalid': "Solo archivos de imagen"},
        widget=forms.FileInput
    )

    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir clase CSS a cada campo del formulario
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control contact-input',
                'placeholder': 'Asunto de tu mensaje'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control contact-textarea',
                'rows': 4,
                'placeholder': 'Escribe tu mensaje aquí'
            })
        }