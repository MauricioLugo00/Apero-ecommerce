from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    """
    Formulario para crear un nuevo pedido con campos personalizados.
    """
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 
            'email', 'address_line_1', 'address_line_2', 
            'country', 'city', 'state'
        ]
    
    # Widgets personalizados para mejorar la presentación
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Ingrese su {self.fields[field].label.lower()}'
            })
