from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm, CustomSignupForm
from .models import UserProfile
from orders.models import Order
from allauth.account.views import SignupView, LoginView, LogoutView, PasswordResetView
#from carts.views import _cart_id
from carts.models import Cart, CartItem

# Vista personalizada de registro utilizando SignupView de django-allauth
class CustomSignupView(SignupView):
    form_class = CustomSignupForm  # Formulario de registro personalizado
    template_name = 'accounts/register.html'  # Plantilla a utilizar para la vista de registro

    # Método para manejar el formulario cuando es válido
    def form_valid(self, form):
        response = super().form_valid(form)
        # Mensaje de éxito después del registro
        messages.success(self.request, 'Te has registrado exitosamente. Por favor verifica tu correo electrónico.')
        return response

# Vista del panel de usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)  # Obtener órdenes del usuario
    orders_count = orders.count()  # Contar órdenes del usuario
    userprofile = UserProfile.objects.get(user_id=request.user.id)  # Obtener perfil del usuario

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)  # Renderizar la plantilla del dashboard con el contexto

# Vista de las órdenes del usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')  # Obtener las órdenes del usuario
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)  # Renderizar la plantilla de las órdenes con el contexto

# Vista para editar el perfil del usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)  # Obtener el perfil del usuario o devolver un 404 si no existe
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Guardar los cambios en el formulario del usuario
            profile_form.save()  # Guardar los cambios en el formulario del perfil
            messages.success(request, 'Su información fue guardada con éxito')  # Mensaje de éxito
            return redirect('edit_profile')  # Redirigir a la misma vista después de guardar
    else:
        user_form = UserForm(instance=request.user)  # Inicializar formulario del usuario con datos actuales
        profile_form = UserProfileForm(instance=userprofile)  # Inicializar formulario del perfil con datos actuales

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)  # Renderizar la plantilla de edición de perfil con el contexto

# Vista para cambiar la contraseña del usuario, requiere que el usuario esté autenticado
@login_required(login_url='account_login')
def change_password(request):
    # Redirigir a la vista de cambio de contraseña de allauth
    return redirect('account_change_password')
