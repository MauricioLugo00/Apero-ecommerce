from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    """
    Formulario para la gestión de reseñas de productos.
    Permite a los usuarios enviar calificaciones y comentarios.
    """
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        
    # Personalización de widgets para mejorar la presentación
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Título de la reseña'
        })
    )
    
    review = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu reseña',
            'rows': 4
        })
    )
    
    rating = forms.FloatField(
        min_value=1.0,
        max_value=5.0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calificación (1-5)'
        })
    )